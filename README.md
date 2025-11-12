# pyKVFinder Webapp

A web application for analyzing biomolecular cavities using **pyKVFinder**. Users can upload PDB files, set analysis parameters, and download detailed results including processed PDBs, TOML data, PDFs, and Excel spreadsheets.

<img width="1113" height="518" alt="image" src="https://github.com/user-attachments/assets/91b22dd7-3023-4ab2-b819-271bbe4d2786" />

---

## Features

- Upload and analyze PDB files through a user-friendly web interface.
- Configure analysis parameters:
  - **Probe Out** (default: 8.0 Å)
  - **Volume Cutoff** (default: 50.0 Å³)
- Automatic generation of:
  - **Results TOML** (detailed cavity analysis)
  - **Processed PDB** files
  - **Histograms PDF** (cavity characteristics)
  - **Pocket Results Excel** (tabulated cavity data)
- Download files directly from the web interface.
- Citation-ready for publications and presentations.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nope-sto/pyKVFinder-Webapp-webapp.git
cd pyKVFinder-webapp
```

2. Create the Python virtual environment from the yml dependencies:

```bash

conda env create -f pocket_analysis.yml

```

3. Activate conda environment

```bash
conda activate pocket_analysis.yml
```

> **Note:** Make sure `pyKVFinder`, `Flask`, `pandas`, and `Werkzeug` are installed.

---

## Usage

1. Start the Flask server:

```bash
python app.py
```

2. Open your browser and go to:

```
http://localhost:8008
```

3. Upload a **PDB file**, adjust optional parameters if needed, and click **Analyze PDB**.

4. Once analysis is complete, download your results from the generated links:

- **Results TOML**: Detailed analysis data
- **Output PDB**: Processed PDB with cavities
- **Histograms PDF**: Visualization of cavity characteristics
- **Pocket Results Excel**: Tabulated cavity metrics

---

## Web Interface

### Upload Page

- File upload input for `.pdb` files.
- Parameter fields for `Probe Out` and `Volume Cutoff`.
- Submit button to start analysis.

### Results Page

- Lists downloadable files.
- Provides instructions for interpreting each output.
- Link to return to upload page.

---

## Project Structure

```
pyKVFinder-webapp/
├─ app.py                  # Flask application
├─ templates/
│  ├─ index.html           # Upload page
│  └─ result.html          # Results page
├─ uploads/                # Temporary uploaded files
├─ results/                # Generated output files
├─ pocket_analysis.yml     # Python dependencies
└─ README.md               # This file
```

---

## Example Usage

1. Upload `example.pdb`.
2. Leave default parameters (`Probe Out = 8.0`, `Volume Cutoff = 50.0`) or adjust them.
3. Click **Analyze PDB**.
4. Download all results from the results page.

---

## Citation

If you use this web app in publications or presentations, please acknowledge Dr. Peter Stockinger for providing access to the webapp and cite:

> da Silva Guerra et al. (2021). *pyKVFinder: an efficient and integrable Python package for biomolecular cavity detection and characterization in data science*. [Nature Methods](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-021-04519-4).  

### ✨ Author
**Peter Stockinger**  
🌐 LinkedIn: https://www.linkedin.com/in/peter-stockinger/

