"""Download the SpaceX dashboard dataset into the local data directory."""

from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

DATASET_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "spacex_launch_dash.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(DATASET_URL, OUTPUT_PATH)
    print(f"Downloaded dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
