# 🌊 Hydrology Data Preprocessing & Feature Engineering

**Course:** Applied Programming and Data Science (APPDS)  
**Student:** Dhananjay Kumar C  
**Assignment:** Data Preprocessing and Feature Engineering in a Hydrology Dataset

---

## 📁 Repository Structure

```
hydrology-preprocessing/
│
├── data/
│   └── rainfall_discharge_dataset.csv   ← Place your Kaggle dataset here
│
├── notebooks/
│   └── hydrology_analysis.ipynb         ← Jupyter Notebook (optional)
│
├── src/
│   └── preprocessing.py                 ← Main Python script
│
├── outputs/
│   └── processed_dataset.csv            ← Generated after running the script
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

**Dataset Name:** Daily Rainfall and River Discharge Dataset  
**Source:** [Kaggle](https://www.kaggle.com/)

### Variables

| Column | Type | Description |
|---|---|---|
| `Rainfall` | Float | Daily rainfall in mm |
| `Discharge` | Float | River discharge in m³/s |
| `Temperature` | Float | Daily temperature in °C |
| `Soil_Moisture` | Float | Soil moisture content (%) |
| `Station` | String | Name of monitoring station |
| `Season` | String | Season (Monsoon/Winter/Summer/Post-Monsoon) |

> ⚠️ **Note:** Download the dataset from Kaggle and place the CSV file inside the `data/` folder as `rainfall_discharge_dataset.csv` before running the script.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hydrology-preprocessing.git
cd hydrology-preprocessing
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Linux/Mac
venv\Scripts\activate           # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python src/preprocessing.py
```

The script will:
1. Load the dataset from `data/`
2. Display basic statistics and missing value counts
3. Impute missing values
4. Detect and report outliers using the IQR method
5. Apply scaling and one-hot encoding
6. Engineer two new features
7. Save the processed dataset to `outputs/processed_dataset.csv`

---

## 🔬 What the Script Does

### 1. Loading the Dataset
Uses `pandas` to load the CSV and display shape, data types, statistics, and missing value counts.

### 2. Imputation of Missing Values
| Variable Type | Method | Reason |
|---|---|---|
| Numerical (`Rainfall`, `Soil_Moisture`) | **Mean Imputation** | Preserves overall distribution |
| Categorical (`Season`) | **Mode Imputation** | Replaces with most frequent category |

### 3. Outlier Detection — IQR Method
Outliers are identified using the **Interquartile Range (IQR)**:

```
Lower Bound = Q1 − 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

> In hydrology, extreme values (floods, heavy rainfall) may be real events — outliers are flagged but **not removed** by default.

### 4. Data Transformations
- **Standardization** — Scales `Rainfall` and `Discharge` to mean=0, std=1 using `StandardScaler`
- **One-Hot Encoding** — Converts the `Season` column into binary dummy variables

### 5. Feature Engineering
| Feature | Formula | Purpose |
|---|---|---|
| `Rainfall_Intensity` | `Rainfall / 24` | Hourly intensity from daily total |
| `Discharge_Rainfall_Ratio` | `Discharge / (Rainfall + 1)` | River response to precipitation |

---

## 📦 Requirements

See `requirements.txt`:

```
pandas
scikit-learn
numpy
matplotlib
seaborn
```

---

## 📌 Key Concepts Covered (Section A)

- Difference between **CSV and JSON** formats
- Importance of **Git version control** in data science
- Resolving **merge conflicts** in GitHub
- **Imputation techniques** for missing data
- **Feature engineering** for model improvement

---

## 🤝 Contributing / Collaboration

If working in a team:
1. Create a new branch: `git checkout -b feature/your-name`
2. Make changes and commit: `git commit -m "Add: description"`
3. Push branch: `git push origin feature/your-name`
4. Open a Pull Request on GitHub

---

## 📄 License

This project is submitted as part of academic coursework. Not licensed for commercial use.
