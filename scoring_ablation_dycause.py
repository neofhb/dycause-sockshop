from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np

from sanity_debug_dycause import (
    Case,
    aggregate_summary,
    apply_param_overrides,
    case_method_row,
    discover_cases,
    dycause_normalize_data,
    dycause_rank,
    final_scores,
    find_graph_path,
    local_window,
    make_case_with_entry_arg,
    path_scores_and_membership,
    pearson_scores,
    rank_by_scores,
    read_matrix_xlsx,
    read_table_xlsx,
    write_csv,
)


LAMBDA_VALUES = [0, 0.1, 0.5, 1, 2, 5, 10, 50, 100]
ROOT = Path(__file__).resolve().parent
DYCAUSE_ROOT = ROOT / "dycause_rca"


def read_dycause_builtin_table(path: Path) -> tuple[list[str], np.ndarray]:
    from sanity_debug_dycause import xlsx_rows

    rows = xlsx_rows(path)
    if not rows:
        raise ValueError(f"{path} is empty")
    headers = [str(row[0]) for row in rows]
    values = []
    for row in rows:
        numeric = [float(value) for value in row[1:] if value is not None]
        values.append(numeric)
    return headers, np.asarray(values, dtype=float).T


def builtin_case_pymicro() -> list[Case]:
    services, _data = read_dycause_builtin_table(DYCAUSE_ROOT / "data" / "pymicro" / "rawdata.xlsx")
    entry_service = "view"
    entry_index = services.index(entry_service)
    root_service = "service1"
    root_index = services.index(root_service)
    return [
        Case(
            case_id="pymicro_builtin",
            dataset_group="dycause_builtin",
            experiment="pymicro",
            run="single",
            run_dir=DYCAUSE_ROOT / "data" / "pymicro",
            metadata_path=DYCAUSE_ROOT / "data" / "pymicro" / "rawdata.xlsx",
            rawdata_path=DYCAUSE_ROOT / "data" / "pymicro" / "rawdata.xlsx",
            services=services,
            entry_service=entry_service,
            entry_index=entry_index,
            dycause_entry_arg=entry_index + 1,
            entry_arg_0based=entry_index,
            entry_arg_1based=entry_index + 1,
            root_service=root_service,
            root_index=root_index,
            root_id=root_index + 1,
            start_time=1200,
            before_length=100,
            after_length=0,
            lag=9,
            step=30,
            edge_thres=0.8,
            dycause_dataset="pymicro",
            dycause_cmd="python main_dycause_mp.py pymicro 16 1 --start 1200 --step 30 --bef 100 --aft 0 --lag 9 --num_sel 1 --edge_thres 0.8 --verbose 2 --mean arithmetic",
            fault_start=1200,
            fault_end=1200,
            topk_path=50,
            num_sel_node=1,
        )
    ]


def normalized_path_plus_pearson(path_score: dict[str, float], pearson_score: dict[str, float]) -> dict[str, float]:
    path_values = list(path_score.values())
    pearson_values = list(pearson_score.values())
    max_path = max(path_values) if path_values else 0.0
    max_pearson = max(pearson_values) if pearson_values else 0.0
    return {
        service: (0.0 if max_path == 0 else path_score.get(service, 0.0) / max_path)
        + (0.0 if max_pearson == 0 else pearson_score.get(service, 0.0) / max_pearson)
        for service in pearson_score
    }


def lambda_score(pearson_score: dict[str, float], path_score: dict[str, float], lam: float) -> dict[str, float]:
    return {
        service: pearson_score.get(service, 0.0) + lam * path_score.get(service, 0.0)
        for service in pearson_score
    }


def case_method_with_scores(
    case: Case,
    method: str,
    scores: dict[str, float],
    path_score: dict[str, float],
    pearson_score: dict[str, float],
    root_in_top_paths: bool,
    graph_source: str = "scoring_ablation",
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    row = case_method_row(
        case,
        method,
        rank_by_scores(scores),
        scores,
        graph_source,
        path_score=path_score,
        pearson_score=pearson_score,
        root_in_top_paths=root_in_top_paths,
    )
    if extra:
        row.update(extra)
    return row


def original_dycause_row(case: Case, local_data: np.ndarray, matrix: np.ndarray) -> dict[str, object]:
    ranked, candidate_scores = dycause_rank(case, matrix, local_data)
    # Keep original DyCause ranking semantics, but expose path/pearson context.
    headers = {
        "case_id": case.case_id,
        "dataset_group": case.dataset_group,
        "experiment": case.experiment,
        "run": case.run,
        "root_service": case.root_service,
        "entry_service": case.entry_service,
        "entry_index_0based": case.entry_index,
        "method": "original_dycause",
        "graph_source": "original_dycause",
        "dycause_entry_arg": case.dycause_entry_arg,
        "entry_arg_zero_based": case.dycause_entry_arg == case.entry_index,
    }
    row = case_method_row(case, "original_dycause", ranked, candidate_scores, "original_dycause")
    row.update(headers)
    return row


def print_report(summary_rows: list[dict[str, object]], detail_rows: list[dict[str, object]], lambda_rows: list[dict[str, object]]) -> None:
    sorted_summary = sorted(summary_rows, key=lambda row: (float(row["mrr"]), float(row["top2"]), float(row["acc"])), reverse=True)
    best_method = sorted_summary[0] if sorted_summary else None
    best_lambda = None
    lambda_only = [row for row in summary_rows if str(row["method"]).startswith("pearson_plus_lambda_path")]
    if lambda_only:
        best_lambda = max(lambda_only, key=lambda row: (float(row["mrr"]), float(row["top2"]), float(row["acc"])))

    pearson_summary = next((row for row in summary_rows if row["method"] == "pearson_only"), None)
    stable_improvements = 0
    if pearson_summary:
        for row in lambda_only:
            if (float(row["top2"]), float(row["mrr"]), float(row["acc"])) > (
                float(pearson_summary["top2"]),
                float(pearson_summary["mrr"]),
                float(pearson_summary["acc"]),
            ):
                stable_improvements += 1

    by_case = defaultdict(dict)
    for row in detail_rows:
        by_case[row["case_id"]][row["method"]] = row
    positive_cases = []
    negative_cases = []
    for case_id, methods in by_case.items():
        pearson = methods.get("pearson_only")
        path_plus = methods.get("path_plus_pearson")
        if not pearson or not path_plus:
            continue
        pearson_tuple = (float(pearson["top2"]), float(pearson["mrr"]), float(pearson["acc"]))
        path_tuple = (float(path_plus["top2"]), float(path_plus["mrr"]), float(path_plus["acc"]))
        if path_tuple > pearson_tuple:
            positive_cases.append(case_id)
        elif path_tuple < pearson_tuple:
            negative_cases.append(case_id)

    print("\n=== Scoring Ablation Report ===")
    if best_method:
        print(
            f"best overall method: {best_method['method']} "
            f"(Top2={float(best_method['top2']):.4f}, Top5={float(best_method['top5']):.4f}, "
            f"MRR={float(best_method['mrr']):.4f}, Acc={float(best_method['acc']):.4f})"
        )
    else:
        print("best overall method: none")
    if best_lambda:
        lam = str(best_lambda["lambda"]) if "lambda" in best_lambda else best_lambda["method"].split("_")[-1]
        print(
            f"best lambda: {lam} "
            f"(Top2={float(best_lambda['top2']):.4f}, Top5={float(best_lambda['top5']):.4f}, "
            f"MRR={float(best_lambda['mrr']):.4f}, Acc={float(best_lambda['acc']):.4f})"
        )
    else:
        print("best lambda: none")
    print(
        "path stable uplift over Pearson: "
        + ("yes" if pearson_summary and stable_improvements >= max(1, len(lambda_only) // 2) else "no")
    )
    print("cases where path helps: " + (", ".join(sorted(positive_cases)) if positive_cases else "none"))
    print("cases where path hurts: " + (", ".join(sorted(negative_cases)) if negative_cases else "none"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Scoring ablation for DyCause path vs Pearson.")
    parser.add_argument("--data-root", default="data\\sockshop_mesh_business")
    parser.add_argument("--output", default="debug_results_scoring")
    parser.add_argument("--entry-service", default="front-end")
    parser.add_argument("--builtin-dataset", default="")
    parser.add_argument("--lag", type=int, default=None)
    parser.add_argument("--step", type=int, default=None)
    parser.add_argument("--edge-thres", type=float, default=None)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    data_root = Path(args.data_root)
    output = Path(args.output)
    if args.builtin_dataset.lower() == "pymicro":
        cases = builtin_case_pymicro()
    else:
        cases = discover_cases(data_root, args.entry_service)
        apply_param_overrides(cases, data_root, args.lag, args.step, args.edge_thres)
    if args.limit:
        cases = cases[: args.limit]

    detail_rows: list[dict[str, object]] = []
    lambda_case_rows: list[dict[str, object]] = []

    for case in cases:
        graph_path = find_graph_path(case)
        if graph_path is None:
            if case.dycause_dataset == "pymicro":
                raise FileNotFoundError(
                    "Missing DyCause graph for pymicro. Run main_dycause_mp.py with the README parameters first."
                )
            continue
        if case.dycause_dataset == "pymicro":
            headers, raw_data = read_dycause_builtin_table(case.rawdata_path)
        else:
            headers, raw_data = read_table_xlsx(case.rawdata_path)
        dycause_data = dycause_normalize_data(raw_data)
        local_data = local_window(dycause_data, case)
        pearson_score = pearson_scores(case, raw_data, headers)
        entry_case = make_case_with_entry_arg(case, case.entry_arg_1based)
        matrix = read_matrix_xlsx(graph_path)
        path_score, root_in_top_paths = path_scores_and_membership(entry_case, matrix)

        detail_rows.append(original_dycause_row(entry_case, local_data, matrix))

        pearson_only_scores = {service: pearson_score.get(service, 0.0) for service in pearson_score}
        path_only_scores = {service: path_score.get(service, 0.0) for service in pearson_score}
        path_plus_scores = final_scores(entry_case, path_score, pearson_score)
        normalized_scores = normalized_path_plus_pearson(path_score, pearson_score)

        detail_rows.append(
            case_method_with_scores(
                entry_case,
                "pearson_only",
                pearson_only_scores,
                path_score,
                pearson_score,
                root_in_top_paths,
            )
        )
        detail_rows.append(
            case_method_with_scores(
                entry_case,
                "path_only",
                path_only_scores,
                path_score,
                pearson_score,
                root_in_top_paths,
            )
        )
        detail_rows.append(
            case_method_with_scores(
                entry_case,
                "path_plus_pearson",
                path_plus_scores,
                path_score,
                pearson_score,
                root_in_top_paths,
            )
        )
        detail_rows.append(
            case_method_with_scores(
                entry_case,
                "normalized_path_plus_pearson",
                normalized_scores,
                path_score,
                pearson_score,
                root_in_top_paths,
            )
        )

        for lam in LAMBDA_VALUES:
            scores = lambda_score(pearson_score, path_score, lam)
            row = case_method_with_scores(
                entry_case,
                f"pearson_plus_lambda_path_{lam}",
                scores,
                path_score,
                pearson_score,
                root_in_top_paths,
                extra={"lambda": lam},
            )
            detail_rows.append(row)
            lambda_case_rows.append(row)

    summary_rows = aggregate_summary(detail_rows)
    lambda_summary = aggregate_summary(lambda_case_rows)
    for row in lambda_summary:
        suffix = str(row["method"]).replace("pearson_plus_lambda_path_", "")
        row["lambda"] = suffix

    write_csv(output / "summary.csv", summary_rows)
    write_csv(output / "case_details.csv", detail_rows)
    write_csv(output / "lambda_sweep.csv", lambda_summary)
    print_report(summary_rows, detail_rows, lambda_summary)
    print(f"\nWrote: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
