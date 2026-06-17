"""
Sanity checks for DyCause SockShop reproduction runs.

This script is intentionally diagnostic-only: it reads existing datasets,
metadata, DyCause logs/results, and cached graph matrices, then writes CSVs and
GraphML files under the requested output directory.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


ROOT = Path(__file__).resolve().parent
DYCAUSE_ROOT = ROOT / "dycause_rca"
if str(DYCAUSE_ROOT) not in sys.path:
    sys.path.insert(0, str(DYCAUSE_ROOT))

DEFAULT_DYCAUSE_PARAMS = {
    "before_length": 300,
    "after_length": 300,
    "lag": 5,
    "step": 30,
    "edge_thres": 0.8,
    "start_time": 315,
    "topk_path": 50,
    "num_sel_node": 3,
}


@dataclass
class Case:
    case_id: str
    dataset_group: str
    experiment: str
    run: str
    run_dir: Path
    metadata_path: Path
    rawdata_path: Path
    services: list[str]
    entry_service: str
    entry_index: int
    dycause_entry_arg: int
    entry_arg_0based: int
    entry_arg_1based: int
    root_service: str
    root_index: int
    root_id: int
    start_time: int
    before_length: int
    after_length: int
    lag: int
    step: int
    edge_thres: float
    dycause_dataset: str
    dycause_cmd: str
    fault_start: int | None
    fault_end: int | None
    topk_path: int
    num_sel_node: int


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def clean_case_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")


def parse_cmd_params(command: str) -> dict[str, object]:
    params: dict[str, object] = {}
    if not command:
        return params
    tokens = command.split()
    # Positional form: main_dycause_mp.py <dataset> <frontend> <root...>
    for i, token in enumerate(tokens):
        if token.endswith("main_dycause_mp.py") or token.endswith("main_dycause.py"):
            if i + 1 < len(tokens):
                params["dataset"] = tokens[i + 1]
            if i + 2 < len(tokens):
                params["frontend"] = int(float(tokens[i + 2]))
            break
    option_map = {
        "--start": "start_time",
        "--bef": "before_length",
        "--aft": "after_length",
        "--lag": "lag",
        "--step": "step",
        "--edge_thres": "edge_thres",
        "--topk": "topk_path",
        "--num_sel": "num_sel_node",
    }
    for option, key in option_map.items():
        if option in tokens:
            value = tokens[tokens.index(option) + 1]
            params[key] = float(value) if "." in value else int(value)
    return params


def column_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref)
    if not letters:
        return 0
    value = 0
    for char in letters.group(0):
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value - 1


def xlsx_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    strings = []
    for si in root.findall("x:si", ns):
        parts = [node.text or "" for node in si.findall(".//x:t", ns)]
        strings.append("".join(parts))
    return strings


def xlsx_sheet_path(zf: zipfile.ZipFile, preferred_sheet: str | None = None) -> str:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    ns = {
        "x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rels = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels_root
        if rel.attrib.get("Type", "").endswith("/worksheet")
    }
    sheets = workbook.find("x:sheets", ns)
    assert sheets is not None
    first_target = None
    def normalize_target(target: str) -> str:
        target = target.lstrip("/")
        if target.startswith("xl/"):
            return target
        return "xl/" + target

    for sheet in sheets.findall("x:sheet", ns):
        rel_id = sheet.attrib[f"{{{ns['r']}}}id"]
        target = rels[rel_id]
        if first_target is None:
            first_target = target
        if preferred_sheet is not None and sheet.attrib.get("name") == preferred_sheet:
            return normalize_target(target)
    return normalize_target(str(first_target))


def xlsx_rows(path: Path, preferred_sheet: str | None = None) -> list[list[object]]:
    with zipfile.ZipFile(path) as zf:
        shared = xlsx_shared_strings(zf)
        sheet_path = xlsx_sheet_path(zf, preferred_sheet)
        root = ET.fromstring(zf.read(sheet_path))
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows: list[list[object]] = []
    for row in root.findall(".//x:sheetData/x:row", ns):
        cells: dict[int, object] = {}
        for cell in row.findall("x:c", ns):
            ref = cell.attrib.get("r", "A1")
            idx = column_index(ref)
            cell_type = cell.attrib.get("t")
            value_node = cell.find("x:v", ns)
            inline_node = cell.find("x:is/x:t", ns)
            if cell_type == "s" and value_node is not None:
                value: object = shared[int(value_node.text or 0)]
            elif cell_type == "inlineStr" and inline_node is not None:
                value = inline_node.text or ""
            elif value_node is not None:
                text = value_node.text or ""
                try:
                    value = float(text)
                except ValueError:
                    value = text
            else:
                value = None
            cells[idx] = value
        if cells:
            max_col = max(cells)
            rows.append([cells.get(i) for i in range(max_col + 1)])
    return rows


def read_table_xlsx(path: Path) -> tuple[list[str], np.ndarray]:
    rows = xlsx_rows(path)
    if not rows:
        raise ValueError(f"{path} is empty")
    headers = [str(value) for value in rows[0] if value is not None]
    values = []
    for row in rows[1:]:
        if row is None:
            continue
        vals = []
        for i in range(len(headers)):
            value = row[i] if i < len(row) else None
            vals.append(np.nan if value is None else float(value))
        if any(not np.isnan(v) for v in vals):
            values.append(vals)
    return headers, np.asarray(values, dtype=float)


def dycause_normalize_data(data: np.ndarray) -> np.ndarray:
    filled = data.copy()
    for j in range(filled.shape[1]):
        for i in range(filled.shape[0]):
            if filled[i, j] == 0 and i >= 1:
                filled[i, j] = filled[i - 1, j]
    for j in range(filled.shape[1] - 1, -1, -1):
        for i in range(filled.shape[0] - 1, -1, -1):
            if filled[i, j] == 0 and i <= filled.shape[0] - 2:
                filled[i, j] = filled[i + 1, j]
    mean = np.nanmean(filled, axis=0, keepdims=True)
    std = np.nanstd(filled, axis=0, keepdims=True)
    std[std == 0] = 1.0
    return (filled - mean) / std


def read_matrix_xlsx(path: Path) -> np.ndarray:
    rows = xlsx_rows(path, preferred_sheet="Sheet1")
    values = []
    for row in rows:
        vals = [0.0 if value is None else float(value) for value in row]
        if vals:
            values.append(vals)
    return np.asarray(values, dtype=float)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        seen = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.append(key)
        fieldnames = seen
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def discover_cases(data_root: Path, entry_service_override: str | None = None) -> list[Case]:
    cases: list[Case] = []
    for metadata_path in sorted(data_root.rglob("metadata.json")):
        run_dir = metadata_path.parent
        rawdata_path = run_dir / "rawdata.xlsx"
        if not rawdata_path.exists():
            continue
        meta = load_json(metadata_path)
        if "services" not in meta or "root_cause_indices" not in meta:
            continue
        services = list(meta["services"])
        cmd_params = parse_cmd_params(meta.get("dycause_cmd", ""))
        entry_service = entry_service_override or services[int(meta.get("frontend_idx", 0))]
        if entry_service not in services:
            raise ValueError(f"entry service {entry_service!r} not in {metadata_path}")
        entry_index = services.index(entry_service)
        dycause_entry_arg = int(cmd_params.get("frontend", meta.get("frontend_idx", entry_index)))
        entry_arg_0based = entry_index
        entry_arg_1based = entry_index + 1

        root_service = meta.get("root_cause")
        raw_root_id = int(meta["root_cause_indices"][0])
        if not root_service:
            root_service = services[raw_root_id] if 0 <= raw_root_id < len(services) else services[raw_root_id - 1]
        root_index = services.index(root_service)
        root_id = raw_root_id

        experiment = meta.get("experiment", run_dir.parent.name)
        run = meta.get("run", run_dir.name if run_dir.name.startswith("run") else "single")
        dycause_dataset = str(cmd_params.get("dataset", meta.get("dycause_dataset", experiment)))
        case_id = clean_case_id(f"{dycause_dataset}_{run}" if run not in dycause_dataset else dycause_dataset)
        fault_start = meta.get("fault_start", meta.get("fault_start_second"))
        fault_end = meta.get("fault_end", meta.get("fault_end_second"))
        cases.append(
            Case(
                case_id=case_id,
                dataset_group=data_root.name,
                experiment=experiment,
                run=run,
                run_dir=run_dir,
                metadata_path=metadata_path,
                rawdata_path=rawdata_path,
                services=services,
                entry_service=entry_service,
                entry_index=entry_index,
                dycause_entry_arg=dycause_entry_arg,
                entry_arg_0based=entry_arg_0based,
                entry_arg_1based=entry_arg_1based,
                root_service=root_service,
                root_index=root_index,
                root_id=root_id,
                start_time=int(cmd_params.get("start_time", meta.get("anomaly_start_second", DEFAULT_DYCAUSE_PARAMS["start_time"]))),
                before_length=int(cmd_params.get("before_length", meta.get("baseline_seconds", DEFAULT_DYCAUSE_PARAMS["before_length"]))),
                after_length=int(cmd_params.get("after_length", meta.get("fault_seconds", DEFAULT_DYCAUSE_PARAMS["after_length"]))),
                lag=int(cmd_params.get("lag", DEFAULT_DYCAUSE_PARAMS["lag"])),
                step=int(cmd_params.get("step", DEFAULT_DYCAUSE_PARAMS["step"])),
                edge_thres=float(cmd_params.get("edge_thres", DEFAULT_DYCAUSE_PARAMS["edge_thres"])),
                dycause_dataset=dycause_dataset,
                dycause_cmd=meta.get("dycause_cmd", ""),
                fault_start=int(fault_start) if fault_start is not None else None,
                fault_end=int(fault_end) if fault_end is not None else None,
                topk_path=int(cmd_params.get("topk_path", DEFAULT_DYCAUSE_PARAMS["topk_path"])),
                num_sel_node=int(cmd_params.get("num_sel_node", DEFAULT_DYCAUSE_PARAMS["num_sel_node"])),
            )
        )
    return cases


def apply_param_overrides(
    cases: list[Case],
    data_root: Path,
    lag: int | None,
    step: int | None,
    edge_thres: float | None,
) -> None:
    default_lag = lag
    default_step = step
    default_edge = edge_thres
    if default_lag is None and default_step is None and default_edge is None:
        if data_root.name == "sockshop_mesh_business":
            default_lag, default_step, default_edge = 5, 30, 0.8
        elif data_root.name == "sockshop_mesh_extended":
            default_lag, default_step, default_edge = 7, 30, 0.8
    for case in cases:
        if default_lag is not None:
            case.lag = default_lag
        if default_step is not None:
            case.step = default_step
        if default_edge is not None:
            case.edge_thres = default_edge


def graph_filename(case: Case, start_time: int | None = None) -> str:
    # DyCause graph filenames do not include start_time; start_time is encoded in
    # the local-results cache. Keep the signature for oracle-window diagnostics.
    _ = start_time
    return (
        f"graph-bef{case.before_length}-aft{case.after_length}"
        f"-step{case.step}-lag{case.lag}-thres{case.edge_thres}.xlsx"
    )


def find_graph_path(case: Case, start_time: int | None = None) -> Path | None:
    result_dir = DYCAUSE_ROOT / "dycause" / "results" / case.dycause_dataset
    exact = result_dir / graph_filename(case, start_time=start_time)
    if exact.exists():
        return exact
    matches = sorted(result_dir.glob(f"graph-bef{case.before_length}-aft{case.after_length}-step{case.step}-lag{case.lag}-thres*.xlsx"))
    if matches:
        return matches[0]
    return None


def run_missing_dycause(case: Case, python_exe: str) -> None:
    if not case.dycause_cmd:
        return
    subprocess.run(case.dycause_cmd, cwd=DYCAUSE_ROOT, shell=True, check=False)


def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float).copy()
    for col_index in range(matrix.shape[1]):
        col_sum = np.sum(matrix[:, col_index])
        if col_sum != 0:
            matrix[:, col_index] = matrix[:, col_index] / col_sum
    return matrix


def dycause_bfs(transition_matrix: np.ndarray, entry_point: int, max_path_length: int | None = None) -> set[tuple[int, ...]]:
    path_list: set[tuple[int, ...]] = set()
    queue = [[entry_point - 1]]
    while queue:
        if len(path_list) > 10000:
            break
        if len(queue) > 10000:
            while queue:
                path_list.add(tuple(queue.pop(0)))
            break
        path = queue.pop(0)
        if np.sum(transition_matrix[:, path[-1]]) == 0:
            path_list.add(tuple(path))
            continue
        if max_path_length is not None and len(path) >= max_path_length:
            path_list.add(tuple(path))
            continue
        for prev_node in range(transition_matrix.shape[0]):
            if transition_matrix[prev_node, path[-1]] > 0.0 and prev_node not in path:
                queue.append(path + [prev_node])
    return path_list


def dycause_paths(
    transition_matrix: np.ndarray,
    entry_point: int,
    max_path_length: int | None = None,
) -> list[tuple[float, tuple[int, ...]]]:
    path_list = dycause_bfs(transition_matrix, entry_point, max_path_length=max_path_length)
    out = []
    for path in path_list:
        probs = []
        end = path[0]
        for start in path[1:]:
            probs.append(transition_matrix[start, end])
            end = start
        out.append((0.0 if not probs else float(np.mean(probs)), path))
    out.sort(key=lambda item: item[0], reverse=True)
    return out


def dycause_ranknode(
    data: np.ndarray,
    out_path: list[tuple[float, tuple[int, ...]]],
    entry_point: int,
    node_num: int,
    topk_path: int = 60,
    prob_thres: float = 0.2,
    num_sel_node: int = 1,
) -> list[list[float]]:
    path_node_count: Counter[int] = Counter()
    for item in out_path[:topk_path]:
        for node in item[1][-num_sel_node:]:
            path_node_count[node] += 1
        if item[0] < prob_thres:
            break
    if entry_point - 1 in path_node_count:
        path_node_count.pop(entry_point - 1)

    path_node_corr = {}
    for node in path_node_count:
        ret = np.corrcoef(
            np.concatenate(
                [data[:, entry_point - 1].reshape(1, -1), data[:, node].reshape(1, -1)],
                axis=0,
            )
        )
        corr = ret[0, 1]
        path_node_corr[node] = 0.0 if not np.isfinite(corr) else abs(float(corr))

    rank_list = []
    for node in path_node_count:
        rank_list.append(
            [
                node + 1,
                path_node_count[node] * 1.0 / (num_sel_node * topk_path) + path_node_corr[node],
            ]
        )
    rank_list.sort(key=lambda item: item[1], reverse=True)
    return rank_list


def dycause_analyze_root(case: Case, matrix: np.ndarray, local_data: np.ndarray) -> list[list[float]]:
    out_path = dycause_paths(matrix, case.dycause_entry_arg)
    return dycause_ranknode(
        local_data,
        out_path,
        case.dycause_entry_arg,
        local_data.shape[1],
        topk_path=case.topk_path,
        prob_thres=0.2,
        num_sel_node=case.num_sel_node,
    )


def make_case_with_entry_arg(case: Case, entry_arg: int) -> Case:
    if entry_arg <= 0:
        raise ValueError(f"DyCause wrapper forbids non-positive entry arg: {entry_arg}")
    cloned = Case(**{field: getattr(case, field) for field in case.__dataclass_fields__})
    cloned.dycause_entry_arg = entry_arg
    return cloned


def make_case_with_entry_arg_unsafe(case: Case, entry_arg: int) -> Case:
    cloned = Case(**{field: getattr(case, field) for field in case.__dataclass_fields__})
    cloned.dycause_entry_arg = entry_arg
    return cloned


def adjacency(matrix: np.ndarray, services: list[str]) -> dict[str, list[str]]:
    graph = {service: [] for service in services}
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > 0:
                graph[services[i]].append(services[j])
    return graph


def save_graphml(path: Path, matrix: np.ndarray, services: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    graphml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    ET.SubElement(graphml, "key", id="d0", **{"for": "node", "attr.name": "index", "attr.type": "int"})
    ET.SubElement(graphml, "key", id="d1", **{"for": "edge", "attr.name": "weight", "attr.type": "double"})
    graph = ET.SubElement(graphml, "graph", id="G", edgedefault="directed")
    for index, service in enumerate(services):
        node = ET.SubElement(graph, "node", id=service)
        data = ET.SubElement(node, "data", key="d0")
        data.text = str(index)
    edge_id = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > 0:
                edge = ET.SubElement(graph, "edge", id=f"e{edge_id}", source=services[i], target=services[j])
                data = ET.SubElement(edge, "data", key="d1")
                data.text = str(float(matrix[i, j]))
                edge_id += 1
    ET.ElementTree(graphml).write(path, encoding="utf-8", xml_declaration=True)


def path_or_blank(graph: dict[str, list[str]], source: str, target: str) -> tuple[bool, str, int | str]:
    if source not in graph or target not in graph:
        return False, "", ""
    queue = [[source]]
    seen = {source}
    while queue:
        path = queue.pop(0)
        if path[-1] == target:
            return True, " -> ".join(path), len(path) - 1
        for neighbor in graph[path[-1]]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(path + [neighbor])
    return False, "", ""


def graph_diagnostics(case: Case, matrix: np.ndarray) -> dict[str, object]:
    graph = adjacency(matrix, case.services)
    root = case.root_service
    entry = case.entry_service
    has_root_to_entry, root_to_entry_path, root_to_entry_len = path_or_blank(graph, root, entry)
    has_entry_to_root, entry_to_root_path, entry_to_root_len = path_or_blank(graph, entry, root)
    out_degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    in_degrees = {node: 0 for node in graph}
    edge_count = 0
    for neighbors in graph.values():
        edge_count += len(neighbors)
        for target in neighbors:
            in_degrees[target] += 1
    return {
        "case_id": case.case_id,
        "experiment": case.experiment,
        "run": case.run,
        "root_service": root,
        "entry_service": entry,
        "root_in_graph": root in graph,
        "root_out_degree": out_degrees[root] if root in graph else "",
        "root_in_degree": in_degrees[root] if root in graph else "",
        "root_has_out_edges": (out_degrees[root] > 0) if root in graph else False,
        "root_has_in_edges": (in_degrees[root] > 0) if root in graph else False,
        "entry_in_graph": entry in graph,
        "entry_out_degree": out_degrees[entry] if entry in graph else "",
        "entry_in_degree": in_degrees[entry] if entry in graph else "",
        "root_to_entry_path_exists": has_root_to_entry,
        "entry_to_root_path_exists": has_entry_to_root,
        "root_to_entry_shortest_path": root_to_entry_path,
        "entry_to_root_shortest_path": entry_to_root_path,
        "root_to_entry_path_len": root_to_entry_len,
        "entry_to_root_path_len": entry_to_root_len,
        "edge_count": edge_count,
        "node_count": len(graph),
        "entry_arg_zero_based": case.dycause_entry_arg == case.entry_index,
        "dycause_entry_arg": case.dycause_entry_arg,
        "actual_entry_index": case.entry_index,
    }


def rank_metrics(case: Case, ranked_services: list[str], scores: dict[str, float] | None = None) -> dict[str, object]:
    rank = ranked_services.index(case.root_service) + 1 if case.root_service in ranked_services else None
    total = len(case.services)
    return {
        "root_rank": "" if rank is None else rank,
        "top1": float(rank == 1) if rank is not None else 0.0,
        "top2": float(rank is not None and rank <= 2),
        "top5": float(rank is not None and rank <= min(5, len(ranked_services))),
        "mrr": 0.0 if rank is None else 1.0 / rank,
        "acc": 0.0 if rank is None else (total - rank + 1) / total,
        "top_services": " > ".join(ranked_services[:10]),
        "root_score": "" if scores is None or case.root_service not in scores else scores[case.root_service],
    }


def rank_ids_to_services(case: Case, ranked_nodes: list[list[float]]) -> tuple[list[str], dict[str, float]]:
    ranked_services: list[str] = []
    scores: dict[str, float] = {}
    for node_id, score in ranked_nodes:
        idx = int(node_id) - 1
        if 0 <= idx < len(case.services):
            service = case.services[idx]
            if service not in ranked_services:
                ranked_services.append(service)
                scores[service] = float(score)
    return ranked_services, scores


def dycause_rank(case: Case, matrix: np.ndarray, local_data: np.ndarray) -> tuple[list[str], dict[str, float]]:
    ranked_nodes = dycause_analyze_root(case, matrix, local_data)
    return rank_ids_to_services(case, ranked_nodes)


def top_paths_rows(case: Case, matrix: np.ndarray, method: str, limit: int = 20) -> list[dict[str, object]]:
    rows = []
    for rank, (weight, path) in enumerate(dycause_paths(matrix, case.dycause_entry_arg)[:limit], start=1):
        services = [case.services[node] for node in path if 0 <= node < len(case.services)]
        rows.append(
            {
                "case_id": case.case_id,
                "experiment": case.experiment,
                "run": case.run,
                "method": method,
                "entry_service": case.entry_service,
                "entry_arg": case.dycause_entry_arg,
                "path_rank": rank,
                "path_weight": weight,
                "path_nodes": " -> ".join(services),
                "contains_root": case.root_service in services,
            }
        )
    return rows


def path_scores_and_membership(case: Case, matrix: np.ndarray) -> tuple[dict[str, float], bool]:
    out_path = dycause_paths(matrix, case.dycause_entry_arg)
    counts: Counter[str] = Counter()
    root_in_top_paths = False
    for probability, path in out_path[: case.topk_path]:
        if probability < 0.2:
            break
        services = [case.services[node] for node in path if 0 <= node < len(case.services)]
        if case.root_service in services:
            root_in_top_paths = True
        for node in path[-case.num_sel_node :]:
            if 0 <= node < len(case.services):
                service = case.services[node]
                if service != case.entry_service:
                    counts[service] += 1
    denominator = float(case.num_sel_node * case.topk_path)
    return (
        {service: counts[service] / denominator for service in candidate_services(case)},
        root_in_top_paths,
    )


def final_scores(case: Case, path_score: dict[str, float], pearson_score: dict[str, float]) -> dict[str, float]:
    # Keep every diagnosable service in the final ranking even when it never
    # appears in the path candidates.
    return {
        service: path_score.get(service, 0.0) + pearson_score.get(service, 0.0)
        for service in candidate_services(case)
    }


def candidate_services(case: Case) -> list[str]:
    return [service for service in case.services if service != case.entry_service]


def pearson_scores(case: Case, data: np.ndarray, headers: list[str]) -> dict[str, float]:
    entry_col = headers.index(case.entry_service)
    entry = data[:, entry_col]
    scores = {}
    for service in candidate_services(case):
        values = data[:, headers.index(service)]
        corr = np.corrcoef(entry, values)[0, 1]
        scores[service] = 0.0 if not np.isfinite(corr) else abs(float(corr))
    return scores


def z_shift_scores(case: Case, data: np.ndarray, headers: list[str], start_time: int | None = None) -> dict[str, float]:
    start = start_time if start_time is not None else case.start_time
    start = min(max(int(start), 1), data.shape[0] - 1)
    baseline = data[:start, :]
    fault = data[start:, :]
    scores = {}
    for service in candidate_services(case):
        col = headers.index(service)
        base = baseline[:, col]
        faulty = fault[:, col]
        std = float(np.nanstd(base))
        shift = abs(float(np.nanmean(faulty)) - float(np.nanmean(base)))
        scores[service] = 0.0 if std == 0 and shift == 0 else (float("inf") if std == 0 else shift / std)
    return scores


def rank_by_scores(scores: dict[str, float]) -> list[str]:
    return sorted(scores, key=lambda service: (-scores[service], service))


def local_window(data: np.ndarray, case: Case, start_time: int | None = None) -> np.ndarray:
    start = case.start_time if start_time is None else start_time
    left = max(0, start - case.before_length)
    right = min(data.shape[0], start + case.after_length)
    return data[left:right, :]


def path_scores(case: Case, matrix: np.ndarray) -> dict[str, float]:
    scores, _root_in_top_paths = path_scores_and_membership(case, matrix)
    return scores


def minmax(scores: dict[str, float]) -> dict[str, float]:
    finite_values = [value for value in scores.values() if np.isfinite(value)]
    if not finite_values:
        return {key: 0.0 for key in scores}
    lo = min(finite_values)
    hi = max(finite_values)
    if math.isclose(lo, hi):
        return {key: 0.0 for key in scores}
    return {key: (scores[key] - lo) / (hi - lo) if np.isfinite(scores[key]) else 1.0 for key in scores}


def combine_scores(*score_maps: dict[str, float]) -> dict[str, float]:
    normalized = [minmax(scores) for scores in score_maps]
    keys = sorted(set().union(*(scores.keys() for scores in normalized)))
    return {key: sum(scores.get(key, 0.0) for scores in normalized) for key in keys}


def topology_path(case: Case) -> Path | None:
    candidates = [
        case.run_dir / "topology.json",
        case.run_dir.parent / "topology.json",
        case.run_dir.parent.parent / "topology.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def oracle_topology_matrix(case: Case, path: Path) -> np.ndarray:
    payload = load_json(path)
    matrix = np.zeros((len(case.services), len(case.services)), dtype=float)
    edges = payload.get("edges", payload if isinstance(payload, list) else [])
    for edge in edges:
        if isinstance(edge, dict):
            src = edge.get("source", edge.get("from"))
            dst = edge.get("target", edge.get("to"))
            weight = float(edge.get("weight", 1.0))
        else:
            src, dst = edge[:2]
            weight = 1.0
        if isinstance(src, str):
            src_idx = case.services.index(src)
        else:
            src_idx = int(src)
        if isinstance(dst, str):
            dst_idx = case.services.index(dst)
        else:
            dst_idx = int(dst)
        matrix[src_idx, dst_idx] = weight
    return normalize_matrix(matrix)


def case_method_row(
    case: Case,
    method: str,
    ranked: list[str],
    scores: dict[str, float] | None,
    graph_source: str = "",
    path_score: dict[str, float] | None = None,
    pearson_score: dict[str, float] | None = None,
    root_in_top_paths: bool | None = None,
) -> dict[str, object]:
    root_metrics = {
        "root_path_score": "" if path_score is None else path_score.get(case.root_service, 0.0),
        "root_pearson_score": "" if pearson_score is None else pearson_score.get(case.root_service, 0.0),
        "root_final_score": "" if scores is None else scores.get(case.root_service, ""),
        "root_in_top_paths": "" if root_in_top_paths is None else root_in_top_paths,
    }
    return {
        "case_id": case.case_id,
        "dataset_group": case.dataset_group,
        "experiment": case.experiment,
        "run": case.run,
        "root_service": case.root_service,
        "entry_service": case.entry_service,
        "entry_index_0based": case.entry_index,
        "method": method,
        "graph_source": graph_source,
        **rank_metrics(case, ranked, scores),
        **root_metrics,
        "dycause_entry_arg": case.dycause_entry_arg,
        "entry_arg_zero_based": case.dycause_entry_arg == case.entry_index,
    }


def aggregate_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(str(row["method"]), str(row.get("graph_source", "")))].append(row)
    summary = []
    for (method, graph_source), items in sorted(groups.items()):
        summary.append(
            {
                "method": method,
                "graph_source": graph_source,
                "cases": len(items),
                "top1": np.mean([float(item["top1"]) for item in items]),
                "top2": np.mean([float(item["top2"]) for item in items]),
                "top5": np.mean([float(item["top5"]) for item in items]),
                "mrr": np.mean([float(item["mrr"]) for item in items]),
                "acc": np.mean([float(item["acc"]) for item in items]),
            }
        )
    return summary


def print_report(detail_rows: list[dict[str, object]]) -> None:
    print("\n=== Entry Fix Report ===")
    by_case = defaultdict(list)
    for row in detail_rows:
        by_case[row["case_id"]].append(row)
    for case_id in sorted(by_case):
        rows = {row["method"]: row for row in by_case[case_id]}
        raw_0 = rows.get("dycause_entry_0based_raw")
        fixed_1 = rows.get("dycause_entry_1based_fixed")
        if raw_0 and fixed_1:
            print(
                f"{case_id}: "
                f"0-based Top2={float(raw_0['top2']):.4f}, Top5={float(raw_0['top5']):.4f}, MRR={float(raw_0['mrr']):.4f}, Acc={float(raw_0['acc']):.4f}; "
                f"1-based Top2={float(fixed_1['top2']):.4f}, Top5={float(fixed_1['top5']):.4f}, MRR={float(fixed_1['mrr']):.4f}, Acc={float(fixed_1['acc']):.4f}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Debug DyCause graph/ranking sanity against simple baselines.")
    parser.add_argument("--data-root", default=str(ROOT / "data"), help="Dataset root to scan for metadata.json/rawdata.xlsx.")
    parser.add_argument("--output", default="debug_results", help="Output directory for CSV and GraphML diagnostics.")
    parser.add_argument("--entry-service", default=None, help="Override entry/front-end service name.")
    parser.add_argument("--lag", type=int, default=None, help="Override DyCause lag for cached graph selection.")
    parser.add_argument("--step", type=int, default=None, help="Override DyCause step for cached graph selection.")
    parser.add_argument("--edge-thres", type=float, default=None, help="Override DyCause edge threshold for cached graph selection.")
    parser.add_argument("--run-missing-dycause", action="store_true", help="Run metadata dycause_cmd when cached graph is missing.")
    parser.add_argument("--python", default=sys.executable, help="Python executable used only with --run-missing-dycause.")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit for quick smoke tests.")
    args = parser.parse_args()

    data_root = Path(args.data_root)
    output = Path(args.output)
    cases = discover_cases(data_root, args.entry_service)
    apply_param_overrides(cases, data_root, args.lag, args.step, args.edge_thres)
    if args.limit:
        cases = cases[: args.limit]

    detail_rows: list[dict[str, object]] = []
    top_paths_output_rows: list[dict[str, object]] = []

    for case in cases:
        graph_path = find_graph_path(case)
        if graph_path is None and args.run_missing_dycause:
            run_missing_dycause(case, args.python)
            graph_path = find_graph_path(case)
        headers, raw_data = read_table_xlsx(case.rawdata_path)
        dycause_data = dycause_normalize_data(raw_data)
        pearson = pearson_scores(case, raw_data, headers)

        if graph_path is None:
            continue

        matrix = read_matrix_xlsx(graph_path)
        entry_cases = [
            ("dycause_entry_0based_raw", make_case_with_entry_arg_unsafe(case, case.entry_arg_0based)),
            ("dycause_entry_1based_fixed", make_case_with_entry_arg(case, case.entry_arg_1based)),
        ]
        for method_name, entry_case in entry_cases:
            local_data = local_window(dycause_data, entry_case)
            path_score, root_in_top_paths = path_scores_and_membership(entry_case, matrix)
            top_paths_output_rows.extend(top_paths_rows(entry_case, matrix, method_name, limit=20))
            final_score = final_scores(entry_case, path_score, pearson)
            ranked = rank_by_scores(final_score)
            detail_rows.append(
                case_method_row(
                    entry_case,
                    method_name,
                    ranked,
                    final_score,
                    "entry_index_experiment",
                    path_score=path_score,
                    pearson_score=pearson,
                    root_in_top_paths=root_in_top_paths,
                )
            )

    summary_rows = aggregate_summary(detail_rows)
    write_csv(output / "summary.csv", summary_rows)
    write_csv(output / "case_details.csv", detail_rows)
    write_csv(output / "top_paths.csv", top_paths_output_rows)
    print_report(detail_rows)
    print(f"\nWrote: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
