"""Simple script to download perf profiling dataset from S3.

Usage:
    cd perf_tests
    poetry install
    poetry run ./run_perf_tests.py

Inline dependency metadata for `uv`:

# /// script
# requires-python = "==3.10"
# dependencies = [
#     "airbyte",  # PyAirbyte
# ]
# ///

"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import airbyte as ab


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.info("Test test test.")

S3_BUCKET_NAME = "airbyte-internal-performance"
S3_OBJECTS_PREFIX = "profiling-input-files/json/no_op_source/stream1/"

SCRIPT_DIR = Path(__file__).resolve().absolute().parent
CONNECTOR_DIR = SCRIPT_DIR.parent
LOCAL_TARGET_DIR = SCRIPT_DIR / Path(".test-data/perf-profile-dataset")
SECRETS_FILE_NAME = SCRIPT_DIR / Path("../secrets/bulk_jsonl_perf_test_config.json")

WARMUP_ITERATIONS = 0
MEASURED_ITERATIONS = 1
NUM_FILES = 1

def main() -> None:
    config_dict = json.loads(Path(SECRETS_FILE_NAME).read_text())

    # Truncate to the specific number of files to test
    config_dict["streams"][0]["globs"] = config_dict["streams"][0]["globs"][:NUM_FILES]

    old_source = ab.get_source(
        "source-s3",
        pip_url="airbyte-source-s3",
        config=config_dict,
        install_root=CONNECTOR_DIR / ".venv-prev-version",
        streams="*",
    )
    Path(CONNECTOR_DIR / ".venv-latest-version").mkdir(parents=True, exist_ok=True)
    new_source = ab.get_source(
        "source-s3",
        pip_url=f"-e {CONNECTOR_DIR.absolute()!s}",
        config=config_dict,
        # local_executable="source-s3",
        install_root=CONNECTOR_DIR / ".venv-latest-version",
        streams="*",
    )

    for i in range(WARMUP_ITERATIONS + MEASURED_ITERATIONS):
        print(f"======Starting prev-version test iteration #{i}======")
        old_source.read(force_full_refresh=True)
        print(f"======Finished prev-version test iteration #{i}======")

    for i in range(WARMUP_ITERATIONS + MEASURED_ITERATIONS):
        print(f"======Starting local-version test iteration #{i}======")
        new_source.read(force_full_refresh=True)
        print(f"======Finished local-version test iteration #{i}======")


if __name__ == "__main__":
    main()