import pandas as pd
from pathlib import Path
from utils.paths import OUTPUT_DIR

def CalculateUrbanGreenIndicators(trees_df: pd.DataFrame, population: int) -> dict:
    if population <= 0:
        raise ValueError("Population must be > 0.")

    per_species = trees_df.copy()
    per_species["trees_per_citizen"] = per_species["total"] / population
    total_trees = int(per_species["total"].sum())
    overall_ratio = total_trees / population

    summary_row = pd.DataFrame({
        "greek_name": ["ΣΥΝΟΛΟ ΔΕΝΤΡΩΝ"],
        "scientific_name": [""],
        "total": [total_trees],
        "trees_per_citizen": [overall_ratio]
    })

    final_df = pd.concat([per_species, summary_row], ignore_index=True)

    results = {
        "per_species": per_species,
        "summary_row": summary_row,
        "final_df": final_df,
        "population": population
    }

    # --- Auto-save ---
    output_file = OUTPUT_DIR / "CalculateUrbanGreenIndicators_output.xlsx"
    final_df.to_excel(output_file, index=False)
    print(f"✅ Saved CalculateUrbanGreenIndicators results to {output_file}")

    return results
