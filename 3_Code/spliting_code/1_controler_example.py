# 3_Code/spliting_code/controller_example.py

from pathlib import Path
import sys

# Add 3_Code/ to the Python import path (so imports work when run directly)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from spliting_code.CleanAndNormalise import CleanAndNormalise
from spliting_code.ExtractPopulationCount import ExtractPopulationCount
from spliting_code.CalculateUrbanGreenIndicators import CalculateUrbanGreenIndicators
from spliting_code.GenerateGraphsAndVisualSummaries import GenerateGraphsAndVisualSummaries
from spliting_code.utils.paths import TREES_FILE, POPULATION_FILE, OUTPUT_EXCEL

def run():
    trees = CleanAndNormalise(TREES_FILE)
    pop = ExtractPopulationCount(POPULATION_FILE, municipality="ΔΗΜΟΣ ΘΕΣΣΑΛΟΝΙΚΗΣ")
    results = CalculateUrbanGreenIndicators(trees, pop)
    outputs = GenerateGraphsAndVisualSummaries(results, OUTPUT_EXCEL)

    print(f"\n✅ Excel: {outputs['excel']}")
    for img in outputs["images"]:
        print(f"✅ Image: {img}")

if __name__ == "__main__":
    run()
