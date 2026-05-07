from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from notebooks.notebook_utils import ensure_binary_file, ensure_text_file


ASSETS = {
    "API_call_spacex_api.json": (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json"
    ),
    "dataset_part_1.csv": (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
    ),
    "dataset_part_2.csv": (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
    ),
    "dataset_part_3.csv": (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv"
    ),
    "Spacex.csv": (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
    ),
    "spacex_launch_geo.csv": (
        "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
        "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
    ),
    "falcon9_wiki_snapshot.html": (
        "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
    ),
}


def main() -> None:
    for filename, url in ASSETS.items():
        if filename.endswith(".html") or filename.endswith(".json"):
            path = ensure_text_file(filename, url)
        else:
            path = ensure_binary_file(filename, url)
        print(f"Synced {path}")


if __name__ == "__main__":
    main()
