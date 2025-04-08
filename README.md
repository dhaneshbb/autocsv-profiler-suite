
# AutoCSV Profiler Suite

[![Watch the demo](assets/video-thumbnail.png)](https://drive.google.com/uc?export=preview&id=1tBFFC_X-lsBJ9PQv4aLpbkTUde1OCtfu)


**CSV Analysis with Isolated Environments**  

Automate exploratory data analysis (EDA) for CSV datasets using **Sweetviz**, **ydata-profiling**, and **DataPrep** without dependency conflicts.  

**Goal**:  

1. **Orchestration & Workflow Management**  
   - `run_analysis.bat`: Batch script to coordinate the analysis workflow.  
     - Activates virtual environments.  
     - Collects user input (CSV path, delimiter, script selection).  
     - Executes Python scripts in sequence.  

2. **Core Analysis Modules**  
   - `recognize_delimiter.py`: Detects CSV delimiter automatically.  
   - `profile_ydata_profiling_report.py`: Generates EDA reports using `ydata-profiling`.  
   - `profile_sweetviz_report.py`: Creates visual EDA reports with Sweetviz.  
   - `profile_dataprep_report.py`: Produces reports using DataPrep.  
   - `cerberus_validator_specific_columns.py`: Validates data against user-defined schemas.  
   - `auto_csv_profiler.py`: Main script for comprehensive analysis:  
     - Data cleaning (duplicates, missing values).  
     - Statistical summaries (skew, kurtosis, outliers).  
     - Visualizations (histograms, box plots, heatmaps).  
     - Relationship analysis (correlation, chi-square, VIF).  

3. **Environment Management**  
   - Virtual environments (`ds_ml`, `sweetz_ydata_profiler`, `dataprep`) to isolate dependencies for different tools.  

4. **Output Artifacts**  
   - Reports: HTML profiles, validation results, statistical summaries.  
   - Visualizations: PNG images (plots, heatmaps).  
   - Structured data: Cleaned CSV files, outlier logs.  

5. **User Interaction**  
   - Interactive prompts for CSV path, delimiter confirmation, and script selection.  
   - Dynamic menus for choosing analyses (e.g., "Run auto_csv_profiler.py? (y/n)").  

---

**Key Features**:  
- **Modular Design**: Scripts are decoupled for flexibility (e.g., run Sweetviz independently).  
- **Error Handling**: Checks for environment activation failures and script errors.  
- **Cross-Tool Integration**: Supports multiple profiling libraries (ydata, Sweetviz, DataPrep).  
- **Automated Workflow**: From delimiter detection to report generation in one batch process.  

**Use Case**:  
Automated exploratory data analysis (EDA) and validation for CSV datasets, ideal for data engineers and analysts needing quick insights without manual coding.

---

## Table of Contents
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup Guide](#setup-guide)
- [Environment Configuration](#environment-configuration)
- [Execution Workflow](#execution-workflow)
- [Output Artifacts](#output-artifacts)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Conflict-Free Virtual Environments**  
- **Auto-Delimiter Detection**  
- **HTML Reports + Visualizations**  
- **Schema Validation (Cerberus)**  
- **Statistical Outlier Detection** 

*Outputs:* Interactive HTML Profiles | Visual Dashboards | Cleaned Datasets  
*Perfect for:* Quick data quality checks, preprocessing pipelines, and reproducible analysis workflows.

---

**Why This Stands Out:**  
-  **Environment Isolation**: Run conflicting tools (e.g., ydata-profiling v4.x + Sweetviz v2.x) side-by-side  
-  **Batch Automation**: Profile 100+ columns with one command  
-  **Portable**: Relative path configuration works across systems  

---

## Directory Structure
```plaintext
AutoCSV-Profiler-Suite/
├── 📂 assets/                # Static resources (e.g., sample CSVs, images)
│   └── bank-additional.csv
├── 📂 batch/                 # Batch orchestration files
│   └── run_analysis.bat
├── 📂 example/               # Sample outputs
│   └── 📂 bank-additional/
│       ├──  profiling_report.html
│       ├──  sweetviz_report.html
│       └── 📁 visualization/
├── 📂 src/                   # Core analysis scripts
│   ├── auto_csv_profiler.py
│   ├── cerberus_validator_specific_columns.py
│   ├── profile_*.py          # All profiling scripts
│   └── recognize_delimiter.py
├──	📂 env/
│	├── 📂 ds_ml/
│	│   └── requirements.txt
│	├── 📂 sweetz_ydata_profiler/
│	│   └── requirements.txt
│	└── 📂 dataprep/
│		└── requirements.txt
├── 📜 MANIFEST.in            # Distribution manifest
├── 📜 README.md              # Project documentation
├── 📜 License             	  # MIT License
```

---

## Setup Guide

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/autocsv-profiler-suite.git
cd autocsv-profiler-suite
```

### 2. Create Virtual Environments
```bash
# Base environment for core analysis
python -m venv env/ds_ml

# Profiling environment (Sweetviz + ydata)
python -m venv env/sweetz_ydata_profiler

# DataPrep environment
python -m venv env/dataprep
```

### 3. Configure Batch File
Edit `batch/run_analysis.bat`:
```bat
set "project_root=%~dp0.."  # Auto-detect root directory
set "env_base=%project_root%\env\ds_ml\Scripts\activate.bat"
set "env_profiling=%project_root%\env\sweetz_ydata_profiler\Scripts\activate.bat"
set "env_dataprep=%project_root%\env\dataprep\Scripts\activate.bat"
```

---

## Environment Configuration

### 1. Base Environment (ds_ml)
```bash
call env/ds_ml/Scripts/activate
pip install pandas==2.0.3 numpy==1.24.3 scipy==1.10.1 seaborn==0.12.2 matplotlib==3.7.2 cerberus==1.3.4 tqdm==4.65.0 scikit-learn==1.3.0
```

### 2. Profiling Environment (sweetz_ydata_profiler)
```bash
call env/sweetz_ydata_profiler/Scripts/activate
pip install ydata-profiling==4.5.1 sweetviz==2.2.1 pandas==1.5.3
```

### 3. DataPrep Environment
```bash
call env/dataprep/Scripts/activate
pip install dataprep==0.4.4 pandas==2.0.3
```

---

## Execution Workflow

### 1. Run Analysis (Sample Dataset)
```bat
cd batch
run_analysis.bat
```
**Inputs When Prompted:**

```
CSV path: ..\assets\bank-additional.csv
Delimiter: ;
Scripts to run: All (y for 1-5)
3. Select scripts to run

+-------+------------------------+--------------------------------------+
| Index | Environment            | Python Script                        |
+-------+------------------------+--------------------------------------+
|   1   | ds_ml                  | auto_csv_profiler.py                 |
|   2   | sweetz_ydata_profiler  | profile_ydata_profiling_report.py    |
|   3   | sweetz_ydata_profiler  | profile_sweetviz_report.py           |
|   4   | dataprep               | profile_dataprep_report.py           |
|   5   | ds_ml                  | cerberus_validator_specific_columns.py|
+-------+------------------------+--------------------------------------+
```

## Scripts Overview

| Script | Environment | Functionality |
|--------|-------------|---------------|
| `profile_ydata_profiling_report.py` | `sweetz_ydata_profiler` | Comprehensive EDA with ydata-profiling |
| `profile_sweetviz_report.py` | `sweetz_ydata_profiler` | Visual comparison reports |
| `profile_dataprep_report.py` | `dataprep` | Interactive HTML dashboards |
| `cerberus_validator_specific_columns.py` | `ds_ml` | Schema-based validation |
| `auto_csv_profiler.py` | `ds_ml` | Statistical summaries + visualizations |


### 2. Monitor Progress
```plaintext
[STATUS] Activating sweetz_ydata_profiler environment...
[PROGRESS] Generating profile_ydata_profiling_report.py |██████████| 100%
```

### 3. Locate Outputs
```plaintext
📂 bank-additional/
├── 📊 profiling_report.html         # ydata output
├── 📈 sweetviz_report.html          # Sweetviz comparison
└── 📁 visualization/                # 50+ analysis plots
```
---

## Output Artifacts

| Category | File Types | Sample Content |
|----------|------------|----------------|
| **Reports** | `.html`, `.txt` | Correlation matrices, missing value analysis |
| **Visualizations** | `.png` | Box plots, histograms, heatmaps |
| **Validation** | `.csv` | Schema violation logs |
| **Cleaned Data** | `.csv` | Imputed/outlier-removed datasets |

---

## Troubleshooting

Add a dedicated section:

| Environment | Key Packages | Version Constraints |
|-------------|--------------|----------------------|
| `ds_ml`     | pandas, scikit-learn | `pandas>=2.0,<3.0` |
| `sweetz_ydata_profiler` | ydata-profiling, sweetviz | `sweetviz==2.2.*` |
| `dataprep`  | dataprep | `dataprep>=0.4.4` |


### **Version Compatibility Notes**
In README's troubleshooting section:

> **Python 3.11 Warning**  
> `ydata-profiling` requires `pandas<2.0`. Use `env/sweetz_ydata_profiler` for compatibility.

### Common Issues
1. **Environment Activation Failures**  
   Verify venv paths in `run_analysis.bat` match your directory structure

2. **Delimiter Detection Errors**  
   Run `recognize_delimiter.py` separately:
   ```bash
   python src/recognize_delimiter.py assets/bank-additional.csv
   ```

3. **Package Conflicts**  
   Recreate affected environment with pinned versions

---

## License
MIT License. See [LICENSE](LICENSE).
