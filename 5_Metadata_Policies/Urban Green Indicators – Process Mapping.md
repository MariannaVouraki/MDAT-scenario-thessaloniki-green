# Urban Green Indicators – Data Analyst Documentation

Αυτό το έγγραφο περιγράφει τα datasets και τις διαδικασίες που χρησιμοποιούνται στο σενάριο *Urban Green Indicators for Thessaloniki*.  
Οι διαδικασίες αντιστοιχίζονται σε έννοιες από τα λεξιλόγια **DPV 2.2** και **ODRL 2.2**.

---

## Datasets

### 1. Κατηγορίες Δέντρων (Urban Tree Categories)
- **Τίτλος (GR):** Κατηγορίες Δέντρων  
- **Τίτλος (EN):** Urban Tree Categories  
- **Περιγραφή:** Το dataset περιλαμβάνει λεπτομερή στοιχεία για την αστική δενδροκομία στο Δήμο Θεσσαλονίκης, με πληροφορίες για τα δέντρα ανά δημοτική κοινότητα, την κατάστασή τους, την κατηγοριοποίηση κατά είδος, καθώς και στατιστικά στοιχεία για πάρκα και κοινόχρηστους χώρους.  
- **Πεδία:** `greek_name`, `scientific_name`, `total`  
- **Μορφή:** Excel (.xlsx)  
- **Πηγή:** Thessaloniki Data Space – [Κατηγορίες Δέντρων](https://tds.okfn.gr/dataset/37)  

---

### 2. Μόνιμος Πληθυσμός Δήμου Θεσσαλονίκης (Resident Population 2021)
- **Τίτλος (GR):** Μόνιμος Πληθυσμός Δήμου Θεσσαλονίκης (2021)  
- **Τίτλος (EN):** Resident Population of the Municipality of Thessaloniki (2021)  
- **Περιγραφή:** Αποτελέσματα της Απογραφής Πληθυσμού-Κατοικιών 2021 (ΕΛΣΤΑΤ), που αφορούν τον μόνιμο πληθυσμό του Δήμου Θεσσαλονίκης.  
- **Πεδία:** `Περιγραφή`, `Μόνιμος πληθυσμός`  
- **Μορφή:** Excel (.xlsx)  
- **Πηγή:** Thessaloniki Data Space – [Μόνιμος Πληθυσμός 2021](https://tds.okfn.gr/dataset/207)  

---

## Data Analyst Process Mapping

Οι κύριες ενέργειες που εκτελεί ο **Data Analyst** και οι αντιστοιχίσεις τους σε DPV/ODRL:

---

### 1. Extract permanent population of Thessaloniki
- **Περιγραφή:** Ανάκτηση της τιμής μόνιμου πληθυσμού για τον Δήμο Θεσσαλονίκης από το dataset.  
- **DPV:** `dpv:Collect`  
- **ODRL:** `odrl:use`  
- **Input dataset:** `dataset:population2021`  
- **Output:** Τιμή πληθυσμού (`dpv-pd:Demographic`)

---

### 2. Clean and filter tree dataset
- **Περιγραφή:** Επιλογή πεδίων (greek_name, scientific_name, total), φιλτράρισμα και τυποποίηση αριθμών.  
- **DPV:** `dpv:Transform`  
- **ODRL:** `odrl:use`  
- **Input dataset:** `dataset:trees`  
- **Output:** Καθαρισμένο dataset δέντρων

---

### 3. Calculate urban green indicators
- **Περιγραφή:** Υπολογισμός δεικτών όπως δέντρα ανά κάτοικο και συνολικός δείκτης πρασίνου.  
- **DPV:** `dpv:Derive`, `dpv:Aggregate`  
- **ODRL:** `odrl:derive`  
- **Inputs:**  
  - `#extract_population` (population value)  
  - `#clean_trees` (cleaned dataset)  
- **Output:** `dataset:indicators` (πίνακας δεικτών)

---

### 4. Produce combined dataset with indicators
- **Περιγραφή:** Συνδυασμός στατιστικών δεικτών σε ολοκληρωμένο dataset με όλα τα αποτελέσματα.  
- **DPV:** `dpv:Derive`, `dpv:Aggregate`  
- **ODRL:** `odrl:derive`  
- **Input:** `#calculate_indicators`  
- **Output:** `dataset:indicators_combined`

---

### 5. Generate visualisations (graphs)
- **Περιγραφή:** Δημιουργία και αποθήκευση γραφημάτων (PNG) με δείκτες πρασίνου (ανά είδος, συνολικά).  
- **DPV:** `dpv:Use`, `dpv:Store`  
- **ODRL:** `odrl:display`, `odrl:store`  
- **Input:** `#produce_combined_dataset`  
- **Outputs:**  
  - `file:trees_per_citizen.png`  
  - `file:trees_per_species.png`  
  - `file:trees_overall.png`

---

## Συνοπτική ροή διαδικασίας
1. **Extract population** →  
2. **Clean trees dataset** →  
3. **Calculate indicators** →  
4. **Produce combined dataset** →  
5. **Generate visualisations**
