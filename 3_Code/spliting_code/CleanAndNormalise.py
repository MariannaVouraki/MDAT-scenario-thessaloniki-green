import pandas as pd
from pathlib import Path
from utils.paths import OUTPUT_DIR

def CleanAndNormalise(trees_path: str | Path) -> pd.DataFrame:
    df = pd.read_excel(trees_path)
    keep_cols = ["greek_name", "scientific_name", "total"]
    out = df[keep_cols].copy()
    out["greek_name"] = out["greek_name"].astype(str).str.strip()
    out["scientific_name"] = out["scientific_name"].astype(str).str.strip()
    out["total"] = pd.to_numeric(out["total"], errors="coerce").fillna(0).astype(int)
    out = out[(out["greek_name"] != "") & (out["total"] > 0)].reset_index(drop=True)

    # --- Auto-save ---
    output_file = OUTPUT_DIR / "CleanAndNormalise_output.csv"
    out.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ Saved CleanAndNormalise results to {output_file}")

    return out
