"""
Run the compressed SockShop mesh fault-type extension batch.

This is the formal extension path after selecting sockshop_mesh_extended as the main
method. It uses only legacy-compressed-v1 load and writes isolated outputs under
data/sockshop_mesh_extended.
"""

import os
import sys

from run_compressed_mesh_batch import main as compressed_main
from run_mesh_experiments import ROOT_DIR


DEFAULT_PLAN = ",".join(f"el_e{index}=1" for index in range(1, 17))
DEFAULT_DATA_ROOT = os.path.join(ROOT_DIR, "data", "sockshop_mesh_extended")


def has_arg(name):
    return any(arg == name or arg.startswith(f"{name}=") for arg in sys.argv[1:])


def main():
    if not has_arg("--plan"):
        sys.argv.extend(["--plan", DEFAULT_PLAN])
    if not has_arg("--data-root"):
        sys.argv.extend(["--data-root", DEFAULT_DATA_ROOT])
    if not has_arg("--dataset-prefix"):
        sys.argv.extend(["--dataset-prefix", "extended_"])
    if not has_arg("--load-profile"):
        sys.argv.extend(["--load-profile", "legacy-compressed-v1"])

    if "--dry-run" in sys.argv:
        print("Reused compressed data is kept in data/sockshop_mesh_extended:")
        print("  mesh_e1: payment Pod-Kill")
        print("  mesh_e3: payment NetworkDelay")
        print("  mesh_e2/mesh_e4/mesh_e5: user/catalogue negative cases")
        print("New extension data will be written under the same extended data root.")

    compressed_main()


if __name__ == "__main__":
    main()
