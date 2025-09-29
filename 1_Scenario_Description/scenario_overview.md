# Scenario: Urban Green Indicators for Thessaloniki

## Context
This scenario analyses the relationship between the permanent population of the Municipality of Thessaloniki and the available urban trees (by species).

It combines:
- Dataset: Resident Population of the Municipality of Thessaloniki (2021) - ( GR - Μόνιμος Πληθυσμός Δήμου Θεσσαλονίκης)
- Dataset: Categories of Urban Trees of the Municipality of Thessaloniki - ( GR - Κατηγορίες Δέντρων)

## Roles (Ontology)
- **Data Provider**: Supplies official datasets (Population census, Tree categories).
- **Data Analyst**: Processes data, executes Python script, generates ratios and graphs.
- **Researcher**: Interprets results for policy/decision-making.

## Workflow
1. **Data Provision**  
   The Data Provider supplies population and tree datasets in Excel format.
2. **Data Processing**  
   The Data Analyst:
   - Extracts permanent population of Thessaloniki
   - Cleans and filters tree dataset (species names, total counts).
   - Calculates urban green indicators(trees per citizen, overall ratio).
   - Produces combined dataset with statistical indicators.
   - Generates visualisations (graphs).
3. **Evaluation**  
   The Researcher reviews results, interprets environmental impact, and links findings to policy.

## Outputs
- Excel file with indicators per species and overall
- Graphs:
  - Trees per citizen (by species)
  - Combined total vs. per species
  - Absolute number of trees per species

