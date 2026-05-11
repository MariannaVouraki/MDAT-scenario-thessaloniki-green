# 3_Code/analysis_script.py
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Το script είναι στο 3_Code/, άρα root = γονικός φάκελος
ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "4_Outputs"

TREES_FILE = DATA_DIR / "Urban Tree Categories.xlsx"
POPULATION_FILE = DATA_DIR / "Permanent Population of the Municipality of Thessaloniki.xlsx"
OUTPUT_EXCEL = OUTPUT_DIR / "trees_per_citizen.xlsx"


# =========================
# mdat:CleanAndNormalise
# =========================
def CleanAndNormalise(trees_path: str | Path) -> pd.DataFrame:
    """
    Διαβάζει το dataset των δέντρων και επιστρέφει καθαρό/ομογενοποιημένο DataFrame
    με στήλες: ['greek_name','scientific_name','total'].
    """
    df = pd.read_excel(trees_path)

    keep_cols = ["greek_name", "scientific_name", "total"]
    missing = [c for c in keep_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Λείπουν στήλες από το trees dataset: {missing}")

    out = df[keep_cols].copy()
    out["greek_name"] = out["greek_name"].astype(str).str.strip()
    out["scientific_name"] = out["scientific_name"].astype(str).str.strip()
    out["total"] = pd.to_numeric(out["total"], errors="coerce").fillna(0).astype(int)

    # Αφαιρούμε γραμμές χωρίς όνομα ή με 0 δέντρα
    out = out[(out["greek_name"] != "") & (out["total"] > 0)].reset_index(drop=True)
    return out


# =========================
# mdat:ExtractPopulationCount
# =========================
def ExtractPopulationCount(pop_path: str | Path,
                           municipality: str = "ΔΗΜΟΣ ΘΕΣΣΑΛΟΝΙΚΗΣ",
                           desc_col: str = "Περιγραφή",
                           pop_col: str = "Μόνιμος πληθυσμός") -> int:
    """
    Εντοπίζει/επιστρέφει τον πληθυσμό του ζητούμενου Δήμου από το population dataset.
    """
    pop_df = pd.read_excel(pop_path)

    for col in (desc_col, pop_col):
        if col not in pop_df.columns:
            raise KeyError(f"Λείπει η στήλη '{col}' από το population dataset.")

    row = pop_df[pop_df[desc_col].astype(str).str.strip() == municipality]
    if row.empty:
        row = pop_df[pop_df[desc_col].astype(str).str.strip().str.lower()
                     == municipality.strip().lower()]

    if row.empty:
        raise ValueError(f"Δεν βρέθηκε '{municipality}' στη στήλη '{desc_col}'.")

    value = str(row.iloc[0][pop_col])  # π.χ. "325.182" ή "325,182"
    value = value.replace(".", "").replace(",", "")
    return int(pd.to_numeric(value, errors="raise"))


# =========================
# mdat:CalculateUrbanGreenIndicators
# =========================
def CalculateUrbanGreenIndicators(trees_df: pd.DataFrame, population: int) -> dict:
    """
    Υπολογίζει:
      - trees_per_citizen ανά είδος
      - συνολικά δέντρα & συνολική αναλογία
    Επιστρέφει dict με:
      - 'per_species', 'summary_row', 'final_df', 'population'
    """
    if population <= 0:
        raise ValueError("Ο πληθυσμός πρέπει να είναι > 0.")

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

    return {
        "per_species": per_species,
        "summary_row": summary_row,
        "final_df": final_df,
        "population": population
    }


# =========================
# mdat:GenerateGraphsAndVisualSummaries
# =========================
def GenerateGraphsAndVisualSummaries(results: dict, output_excel_path: str | Path) -> dict:
    """
    Αποθηκεύει το final_df σε Excel και δημιουργεί 3 γραφήματα (.png) μέσα στο 4_Outputs.
    """
    final_df = results["final_df"]
    per_species = results["per_species"]
    summary_row = results["summary_row"]

    output_excel_path = Path(output_excel_path)
    output_dir = output_excel_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Excel
    final_df.to_excel(output_excel_path, index=False)

    # 2) Graph 1 — Trees per citizen (by species)
    plt.style.use("seaborn-v0_8-whitegrid")
    max_bars = 15
    trees_sorted = per_species.sort_values(by="trees_per_citizen", ascending=False).head(max_bars)
    img1 = output_dir / f"{output_excel_path.stem}_per_species.png"

    height = max(8, 0.6 * len(trees_sorted) + 6)
    fig, ax = plt.subplots(figsize=(14, height))
    bars = ax.barh(trees_sorted["greek_name"], trees_sorted["trees_per_citizen"], color="#4C72B0")
    ax.set_xlabel("Δέντρα ανά κάτοικο", fontsize=14)
    ax.set_ylabel("Είδος δέντρου (ελληνικά)", fontsize=14)
    ax.set_title("Αναλογία δέντρων ανά κάτοικο (top 15 είδη)", fontsize=16, pad=14)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=10)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.bar_label(bars, fmt="{:.4f}", padding=4, fontsize=9)
    fig.tight_layout(pad=2.0)
    fig.savefig(img1, dpi=300)
    plt.close(fig)

    # 3) Graph 2 — Overall + species
    trees_with_total = pd.concat([summary_row, trees_sorted], ignore_index=True)
    img2 = output_dir / f"{output_excel_path.stem}_overall_with_species.png"

    height = max(8, 0.6 * len(trees_with_total) + 6)
    fig, ax = plt.subplots(figsize=(14, height))
    colors = ["#1b5e20" if name == "ΣΥΝΟΛΟ ΔΕΝΤΡΩΝ" else "#ff7f0e" for name in trees_with_total["greek_name"]]
    bars = ax.barh(trees_with_total["greek_name"], trees_with_total["trees_per_citizen"], color=colors)
    ax.set_xlabel("Δέντρα ανά κάτοικο", fontsize=14)
    ax.set_ylabel("Είδος δέντρου (ελληνικά)", fontsize=14)
    ax.set_title("Συνολική και αναλυτική αναλογία δέντρων ανά κάτοικο (top 15 είδη)", fontsize=16, pad=14)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=10)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.bar_label(bars, fmt="{:.4f}", padding=4, fontsize=9)
    fig.tight_layout(pad=2.0)
    fig.savefig(img2, dpi=300)
    plt.close(fig)

    # 4) Graph 3 — Absolute number of trees per species
    trees_sorted_total = per_species.sort_values(by="total", ascending=False).head(max_bars)
    img3 = output_dir / f"{output_excel_path.stem}_total_per_species.png"

    height = max(8, 0.6 * len(trees_sorted_total) + 6)
    fig, ax = plt.subplots(figsize=(14, height))
    bars = ax.barh(trees_sorted_total["greek_name"], trees_sorted_total["total"], color="#2a9d8f")
    ax.set_xlabel("Πλήθος δέντρων", fontsize=14)
    ax.set_ylabel("Είδος δέντρου (ελληνικά)", fontsize=14)
    ax.set_title("Συνολικό πλήθος δέντρων ανά είδος (top 15 είδη)", fontsize=16, pad=14)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=10)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.bar_label(bars, fmt="{:,}", padding=4, fontsize=9)
    fig.tight_layout(pad=2.0)
    fig.savefig(img3, dpi=300)
    plt.close(fig)

    return {"excel": str(output_excel_path), "images": [str(img1), str(img2), str(img3)]}


# =========================
# Main pipeline (binds the 4 mdat steps)
# =========================
def main():
    trees_clean = CleanAndNormalise(TREES_FILE)
    population = ExtractPopulationCount(POPULATION_FILE, municipality="ΔΗΜΟΣ ΘΕΣΣΑΛΟΝΙΚΗΣ")
    print(f"✅ Πληθυσμός Δήμου Θεσσαλονίκης: {population:,}".replace(",", "."))

    results = CalculateUrbanGreenIndicators(trees_clean, population)
    outputs = GenerateGraphsAndVisualSummaries(results, OUTPUT_EXCEL)

    print(f"✅ Αποθήκευση Excel: {outputs['excel']}")
    for img in outputs["images"]:
        print(f"✅ Γράφημα: {img}")


if __name__ == "__main__":
    main()
