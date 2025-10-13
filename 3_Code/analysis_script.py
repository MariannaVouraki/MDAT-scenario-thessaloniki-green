import pandas as pd
import matplotlib.pyplot as plt
import os

# === File paths ===
trees_file = "data/Urban Tree Categories.xlsx"
population_file = "data/Permanent Population of the Municipality of Thessaloniki.xlsx"
output_file = "4_Outputs/trees_per_citizen.xlsx"

# === Step 1: Load data ===
trees_df = pd.read_excel(trees_file)
population_df = pd.read_excel(population_file)

# === Step 2: Find population of Municipality of Thessaloniki ===
row = population_df[population_df["Περιγραφή"].astype(str).str.strip() == "ΔΗΜΟΣ ΘΕΣΣΑΛΟΝΙΚΗΣ"]
if row.empty:
    raise ValueError("❌ Δεν βρέθηκε γραμμή με 'ΔΗΜΟΣ ΘΕΣΣΑΛΟΝΙΚΗΣ' στη στήλη 'Περιγραφή'!")

population_str = str(row["Μόνιμος πληθυσμός"].values[0])
population = int(population_str.replace(".", "").replace(",", ""))
print(f"✅ Πληθυσμός Δήμου Θεσσαλονίκης: {population}")

# === Step 3: Clean tree dataset ===
trees_clean = trees_df[["greek_name", "scientific_name", "total"]].copy()

# === Step 4: Calculate trees per citizen (per species) ===
trees_clean["trees_per_citizen"] = trees_clean["total"] / population

# === Step 5: Calculate overall indicator ===
total_trees = trees_clean["total"].sum()
overall_ratio = total_trees / population

summary_row = pd.DataFrame({
    "greek_name": ["ΣΥΝΟΛΟ ΔΕΝΤΡΩΝ"],
    "scientific_name": [""],
    "total": [total_trees],
    "trees_per_citizen": [overall_ratio]
})

final_df = pd.concat([trees_clean, summary_row], ignore_index=True)

# === Step 6: Save results to Excel ===
os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_df.to_excel(output_file, index=False)
print(f"✅ Το αποτέλεσμα αποθηκεύτηκε στο αρχείο: {output_file}")

# === Step 7: Graph 1 – Trees per citizen (by species) ===
trees_sorted = trees_clean.sort_values(by="trees_per_citizen", ascending=False)

plt.figure(figsize=(12, 10))
plt.barh(trees_sorted["greek_name"], trees_sorted["trees_per_citizen"])
plt.xlabel("Δέντρα ανά κάτοικο", fontsize=12)
plt.ylabel("Είδος δέντρου (ελληνικά)", fontsize=12)
plt.title("Αναλογία δέντρων ανά κάτοικο (ανά είδος)", fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=6)
plt.gca().invert_yaxis()
plt.tight_layout()

image_file1 = os.path.splitext(output_file)[0] + "_per_species.png"
plt.savefig(image_file1, dpi=300)
plt.close()
print(f"✅ Γράφημα 1 αποθηκεύτηκε ως: {image_file1}")

# === Step 8: Graph 2 – Overall + species ===
trees_with_total = pd.concat([summary_row, trees_sorted], ignore_index=True)

plt.figure(figsize=(12, 10))
plt.barh(
    trees_with_total["greek_name"],
    trees_with_total["trees_per_citizen"],
    color=["darkgreen"] + ["steelblue"] * len(trees_sorted)
)
plt.xlabel("Δέντρα ανά κάτοικο", fontsize=12)
plt.ylabel("Είδος δέντρου (ελληνικά)", fontsize=12)
plt.title("Συνολική και αναλυτική αναλογία δέντρων ανά κάτοικο", fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=6)
plt.gca().invert_yaxis()
plt.tight_layout()

image_file2 = os.path.splitext(output_file)[0] + "_overall_with_species.png"
plt.savefig(image_file2, dpi=300)
plt.close()
print(f"✅ Γράφημα 2 αποθηκεύτηκε ως: {image_file2}")

# === Step 9: Graph 3 – Absolute number of trees per species ===
trees_sorted_total = trees_clean.sort_values(by="total", ascending=False)

plt.figure(figsize=(12, 10))
plt.barh(trees_sorted_total["greek_name"], trees_sorted_total["total"], color="forestgreen")
plt.xlabel("Πλήθος δέντρων", fontsize=12)
plt.ylabel("Είδος δέντρου (ελληνικά)", fontsize=12)
plt.title("Συνολικό πλήθος δέντρων ανά είδος", fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=6)
plt.gca().invert_yaxis()
plt.tight_layout()

image_file3 = os.path.splitext(output_file)[0] + "_total_per_species.png"
plt.savefig(image_file3, dpi=300)
plt.close()
print(f"✅ Γράφημα 3 αποθηκεύτηκε ως: {image_file3}")
