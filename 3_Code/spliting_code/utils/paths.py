from pathlib import Path

def _detect_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "3_Code").exists() and (p / "data").exists():
            return p
    return here.parents[2]

ROOT = _detect_root()
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "4_Outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TREES_FILE = DATA_DIR / "Urban Tree Categories.xlsx"
POPULATION_FILE = DATA_DIR / "Permanent Population of the Municipality of Thessaloniki.xlsx"
OUTPUT_EXCEL = OUTPUT_DIR / "trees_per_citizen.xlsx"
