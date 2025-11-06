# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # ensure PNGs save in any environment
import matplotlib.pyplot as plt

# use relative import (works reliably inside the package)
from .utils.paths import OUTPUT_DIR

def GenerateGraphsAndVisualSummaries(results: dict, output_excel_path: str | Path | None = None) -> dict:
    """
    Saves final_df to Excel and generates 3 PNGs in OUTPUT_DIR:
      1) <stem>_per_species.png
      2) <stem>_overall_with_species.png
      3) <stem>_total_per_species.png
    """
    if output_excel_path is None:
        output_excel_path = OUTPUT_DIR / "GenerateGraphsAndVisualSummaries_output.xlsx"

    # unpack
    final_df = results["final_df"]
    per_species = results["per_species"]
    summary_row = results["summary_row"]

    # minimal checks (helps detect silent failures)
    for name, df in [("final_df", final_df), ("per_species", per_species), ("summary_row", summary_row)]:
        if not isinstance(df, pd.DataFrame) or df.empty:
            raise ValueError(f"{name} missing or empty")
    for col in ["greek_name", "trees_per_citizen"]:
        if col not in per_species.columns:
            raise KeyError(f"per_species missing column: {col}")
    if "total" not in per_species.columns:
        raise KeyError("per_species missing column: total")

    # ensure paths
    output_excel_path = Path(output_excel_path)
    output_excel_path.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # write Excel
    final_df.to_excel(output_excel_path, index=False)

    stem = output_excel_path.stem

    # --- Graph 1: trees per citizen (by species)
    trees_sorted = per_species.sort_values("trees_per_citizen", ascending=False)
    img1 = OUTPUT_DIR / f"{stem}_per_species.png"
    plt.figure(figsize=(10, 8))
    plt.barh(trees_sorted["greek_name"], trees_sorted["trees_per_citizen"])
    plt.gca().invert_yaxis()
    plt.title("Δέντρα ανά κάτοικο (ανά είδος)")
    plt.tight_layout()
    plt.savefig(img1, dpi=300)
    plt.close()

    # --- Graph 2: overall (summary row) + species
    trees_with_total = pd.concat([summary_row, trees_sorted], ignore_index=True)
    img2 = OUTPUT_DIR / f"{stem}_overall_with_species.png"
    plt.figure(figsize=(10, 8))
    plt.barh(trees_with_total["greek_name"], trees_with_total["trees_per_citizen"])
    plt.gca().invert_yaxis()
    plt.title("Συνολική και αναλυτική αναλογία δέντρων ανά κάτοικο")
    plt.tight_layout()
    plt.savefig(img2, dpi=300)
    plt.close()

    # --- Graph 3: absolute totals per species
    trees_sorted_total = per_species.sort_values("total", ascending=False)
    img3 = OUTPUT_DIR / f"{stem}_total_per_species.png"
    plt.figure(figsize=(10, 8))
    plt.barh(trees_sorted_total["greek_name"], trees_sorted_total["total"])
    plt.gca().invert_yaxis()
    plt.title("Συνολικό πλήθος δέντρων ανά είδος")
    plt.tight_layout()
    plt.savefig(img3, dpi=300)
    plt.close()

    print(f"✅ Saved Excel and graphs to: {OUTPUT_DIR}")
    return {"excel": str(output_excel_path), "images": [str(img1), str(img2), str(img3)]}
