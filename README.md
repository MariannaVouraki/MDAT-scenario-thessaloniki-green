# MDAT Scenario – Thessaloniki Urban Green Indicators

This repository documents the **Urban Green Indicators pilot scenario** for Thessaloniki, including semantic descriptions of datasets and processing operations. The work uses the [Data Privacy Vocabulary (DPV 2.2)](https://w3c.github.io/dpv/2.2/dpv/) and the [ODRL Information Model (2.2)](https://www.w3.org/TR/odrl-model/) to align processes and entities with standard vocabularies.

---

## 📂 Datasets

### 1. Urban Tree Categories (Κατηγορίες Δέντρων)
- **Source:** [Thessaloniki Data Space](https://tds.okfn.gr/dataset/37)  
- **Category (DPV):** `dpv:EnvironmentalData`  
- **Fields:** `greek_name`, `scientific_name`, `total`  
- **Format:** Excel (.xlsx)  
- **License:** ODbL 1.0  

### 2. Resident Population of Thessaloniki Municipality (2021) (Μόνιμος Πληθυσμός Δήμου Θεσσαλονίκης)
- **Source:** [Thessaloniki Data Space](https://tds.okfn.gr/dataset/207)  
- **Category (DPV-PD):** `dpv:DemographicData`  
- **Fields:** `Περιγραφή` (Description), `Μόνιμος πληθυσμός` (Permanent Population)  
- **Format:** Excel (.xlsx)  
- **License:** ODbL 1.0  

### 3. Derived Data
- **Excel Results:** `trees_per_citizen.xlsx` → `dpv:DerivedData`  
- **Graphs (PNG):** Ratio charts → `dpv:VisualisationData`  

---

## ⚙️ Processing Operations

The **Data Analyst** performs the following actions. Each action is described with DPV classes and ODRL actions.

| Step | Description | DPV | ODRL |
|------|-------------|-----|------|
| 1 | Extracts permanent population of Thessaloniki | `dpv:Collect`, `dpv-pd:Demographic` | `odrl:use` |
| 2 | Cleans and filters tree dataset (species names, total counts) | `dpv:Transform` | `odrl:use` |
| 3 | Calculates urban green indicators (trees per citizen, overall ratio) | `dpv:Derive`, `dpv:Aggregate` | `odrl:derive` |
| 4 | Produces combined dataset with statistical indicators | `dpv:Derive`, `dpv:Aggregate` | `odrl:derive` |
| 5 | Generates visualisations (graphs) | `dpv:Store`, `dpv:Use` | `odrl:reproduce`, `odrl:display` |

---

## 🗂 Repository Files

- `2_Data_Specification/datasets.jsonld` → Semantic description of datasets (DPV + domain-specific concepts)  
- `2_Data_Specification/datasets.md` → Human-readable description of datasets  
- `5_Metadata_Policies/entities.jsonld` → Entities (datasets, derived data, roles)  
- `5_Metadata_Policies/processing_operations.jsonld` → Processing operations (DPV + ODRL)  
- `5_Metadata_Policies/Urban Green Indicators – Process Mapping.md` → Human-readable mapping of processes  

---

## 🌱 Domain-Specific Concepts (MDAT)

Additional domain-specific concepts (namespace: `mdat:`) were introduced to specialize the datasets and their properties beyond the generic DPV/ODRL terms.

| Element | Description | MDAT Concept |
|----------|-------------|--------------|
| **Urban Tree** | Represents an urban tree as a data unit | `mdat:UrbanTree` |
| **Tree Category** | Categorisation of trees by species | `mdat:TreeCategory` |
| **Population Count** | Total permanent population of the Municipality | `mdat:PopulationCount` |

---

## ✅ Notes

- All **processing operations** can be described using existing DPV and ODRL concepts.  
- Additional **domain-specific ontology** was only introduced for dataset semantics where DPV/ODRL were too general.  
- Extension to MDAT-specific terms is possible in the future if finer granularity is needed (e.g. `ExtractSubset`, `CleanDataset` refinements).  
