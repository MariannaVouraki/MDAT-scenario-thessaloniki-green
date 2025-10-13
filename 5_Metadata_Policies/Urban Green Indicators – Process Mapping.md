# Urban Green Indicators – Data Analyst Documentation

This document describes the datasets and processes used in the *Urban Green Indicators for Thessaloniki* scenario.  
The processes are mapped to concepts from the **DPV 2.2** and **ODRL 2.2** vocabularies.

---

## Datasets

### 1. Urban Tree Categories
- **Title (GR):** Κατηγορίες Δέντρων  
- **Title (EN):** Urban Tree Categories  
- **Description:** The dataset includes detailed information on urban forestry in the Municipality of Thessaloniki, providing data about trees by municipal community, their condition, species classification, and statistical information about parks and public green spaces.  
- **Fields:** `greek_name`, `scientific_name`, `total`  
- **Format:** Excel (.xlsx)  
- **Source:** Thessaloniki Data Space – [Urban Tree Categories](https://tds.okfn.gr/dataset/37)  

---

### 2. Resident Population of the Municipality of Thessaloniki (2021)
- **Title (GR):** Μόνιμος Πληθυσμός Δήμου Θεσσαλονίκης (2021)  
- **Title (EN):** Resident Population of the Municipality of Thessaloniki (2021)  
- **Description:** Results of the 2021 Population and Housing Census (ELSTAT) referring to the permanent population of the Municipality of Thessaloniki.  
- **Fields:** `Description`, `Permanent population`  
- **Format:** Excel (.xlsx)  
- **Source:** Thessaloniki Data Space – [Resident Population 2021](https://tds.okfn.gr/dataset/207)  

---

## Data Analyst Process Mapping

The main activities performed by the **Data Analyst** and their mappings to DPV/ODRL concepts are as follows:

---

### 1. Extract permanent population of Thessaloniki
- **Description:** Retrieve the permanent population value for the Municipality of Thessaloniki from the dataset.  
- **DPV:** `dpv:Collect`  
- **ODRL:** `odrl:use`  
- **Input dataset:** `dataset:population2021`  
- **Output:** Population value (`dpv-pd:Demographic`)

---

### 2. Clean and filter tree dataset
- **Description:** Select fields (`greek_name`, `scientific_name`, `total`), filter data, and normalize numeric values.  
- **DPV:** `dpv:Transform`  
- **ODRL:** `odrl:use`  
- **Input dataset:** `dataset:trees`  
- **Output:** Cleaned tree dataset  

---

### 3. Calculate urban green indicators
- **Description:** Calculate indicators such as trees per resident and total green index.  
- **DPV:** `dpv:Derive`, `dpv:Aggregate`  
- **ODRL:** `odrl:derive`  
- **Inputs:**  
  - `#extract_population` (population value)  
  - `#clean_trees` (cleaned dataset)  
- **Output:** `dataset:indicators` (indicator table)  

---

### 4. Produce combined dataset with indicators
- **Description:** Combine statistical indicators into a complete dataset containing all results.  
- **DPV:** `dpv:Derive`, `dpv:Aggregate`  
- **ODRL:** `odrl:derive`  
- **Input:** `#calculate_indicators`  
- **Output:** `dataset:indicators_combined`  

---

### 5. Generate visualisations (graphs)
- **Description:** Create and store graphs (PNG) visualizing green indicators (by species, per resident, overall).  
- **DPV:** `dpv:Use`, `dpv:Store`  
- **ODRL:** `odrl:display`, `odrl:reproduce`  
- **Input:** `#produce_combined_dataset`  
- **Outputs:**  
  - `file:trees_per_citizen.png`  
  - `file:trees_per_species.png`  
  - `file:trees_overall.png`  

---

## Summary of Process Flow
1. **Extract population** →  
2. **Clean trees dataset** →  
3. **Calculate indicators** →  
4. **Produce combined dataset** →  
5. **Generate visualisations**
