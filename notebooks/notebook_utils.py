from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen


def project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "data").exists() and (candidate / "notebooks").exists():
            return candidate
    return current


ROOT = project_root()
DATA_DIR = ROOT / "data"


def data_path(filename: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / filename


def ensure_text_file(filename: str, url: str, encoding: str = "utf-8") -> Path:
    destination = data_path(filename)
    if not destination.exists():
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request) as response:
            destination.write_text(response.read().decode(encoding), encoding=encoding)
    return destination


def ensure_binary_file(filename: str, url: str) -> Path:
    destination = data_path(filename)
    if not destination.exists():
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request) as response:
            destination.write_bytes(response.read())
    return destination
