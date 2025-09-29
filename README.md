# MDAT Scenario – Thessaloniki Urban Green Indicators

This repository documents the **Urban Green Indicators pilot scenario** for Thessaloniki, including semantic descriptions of datasets and processing operations. The work uses the [Data Privacy Vocabulary (DPV 2.2)](https://w3c.github.io/dpv/2.2/dpv/) and the [ODRL Information Model (2.2)](https://www.w3.org/TR/odrl-model/) to align processes and entities with standard vocabularies.

---

## 📂 Datasets

### 1. Κατηγορίες Δέντρων (Urban Tree Categories)
- **Source:** [Thessaloniki Data Space](https://tds.okfn.gr/dataset/37)  
- **Category (DPV):** `dpv:EnvironmentalData`  
- **Fields:** `greek_name`, `scientific_name`, `total`  
- **Format:** Excel (.xlsx)  
- **License:** ODbL 1.0  

### 2. Μόνιμος Πληθυσμός Δήμου Θεσσαλονίκης (Resident Population 2021)
- **Source:** [Thessaloniki Data Space](https://tds.okfn.gr/dataset/207)  
- **Category (DPV-PD):** `dpv:DemographicData`  
- **Fields:** `Περιγραφή`, `Μόνιμος πληθυσμός`  
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

Στο σενάριο χρησιμοποιήθηκαν επιπλέον domain-specific έννοιες (namespace: `mdat:`) για να εξειδικεύσουν τα datasets και τα πεδία τους, πέρα από τα γενικά DPV/ODRL terms.

| Στοιχείο | Περιγραφή | MDAT Concept |
|----------|------------|--------------|
| **Urban Tree** | Αναπαριστά αστικό δέντρο ως μονάδα δεδομένων | `mdat:UrbanTree` |
| **Tree Category** | Κατηγοριοποίηση δέντρων ανά είδος | `mdat:TreeCategory` |
| **Population Count** | Συνολικός πληθυσμός Δήμου | `mdat:PopulationCount` |


---
## ✅ Notes

- All **processing operations** can be described using existing DPV and ODRL concepts.  
- No additional **domain-specific ontology** was required for this pilot.  
- Extension to MDAT-specific terms is possible in future if finer granularity is needed (e.g. `ExtractSubset`, `CleanDataset` refinements).  
