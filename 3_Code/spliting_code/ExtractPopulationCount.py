import pandas as pd
from pathlib import Path
from utils.paths import OUTPUT_DIR

def ExtractPopulationCount(pop_path: str | Path,
                           municipality: str = "ΔΗΜΟΣ ΘΕΣΣΑΛΟΝΙΚΗΣ",
                           desc_col: str = "Περιγραφή",
                           pop_col: str = "Μόνιμος πληθυσμός") -> int:
    pop_df = pd.read_excel(pop_path)
    row = pop_df[pop_df[desc_col].astype(str).str.strip() == municipality]
    if row.empty:
        row = pop_df[pop_df[desc_col].astype(str).str.strip().str.lower()
                     == municipality.strip().lower()]

    value = str(row.iloc[0][pop_col])
    value = value.replace(".", "").replace(",", "")
    population = int(pd.to_numeric(value, errors="raise"))

    # --- Auto-save ---
    output_file = OUTPUT_DIR / "ExtractPopulationCount_output.txt"
    output_file.write_text(str(population), encoding="utf-8")
    print(f"✅ Saved population value to {output_file}")

    return population
