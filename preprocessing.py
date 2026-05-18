# ============================================================
# APPDS Assignment - Data Preprocessing & Feature Engineering
# Student: Dhananjay Kumar C
# Dataset: Daily Rainfall and River Discharge Dataset (Kaggle)
# ============================================================

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# ──────────────────────────────────────────────
# SECTION 1: LOAD DATASET
# ──────────────────────────────────────────────

DATA_PATH = os.path.join("data", "rainfall_discharge_dataset.csv")
OUTPUT_PATH = os.path.join("outputs", "processed_dataset.csv")

print("=" * 55)
print("  HYDROLOGY DATA PREPROCESSING PIPELINE")
print("=" * 55)

# Load the dataset
data = pd.read_csv(DATA_PATH)

print("\n📂 Dataset Loaded Successfully!")
print(f"   Shape: {data.shape[0]} rows × {data.shape[1]} columns\n")

# Display first few rows
print("── First 5 Rows ──────────────────────────────────────")
print(data.head())

# Dataset info (dtypes, non-null counts)
print("\n── Dataset Info ──────────────────────────────────────")
print(data.info())

# Statistical summary of numerical columns
print("\n── Statistical Summary ───────────────────────────────")
print(data.describe().round(2))

# Missing value counts
print("\n── Missing Values per Column ─────────────────────────")
print(data.isnull().sum())


# ──────────────────────────────────────────────
# SECTION 2: IMPUTATION OF MISSING VALUES
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("  STEP 2: IMPUTATION")
print("=" * 55)

# --- Numerical columns: Mean Imputation ---
numerical_cols = ['Rainfall', 'Discharge', 'Temperature', 'Soil_Moisture']

for col in numerical_cols:
    if col in data.columns and data[col].isnull().sum() > 0:
        mean_val = data[col].mean()
        data[col] = data[col].fillna(mean_val)
        print(f"   ✔ '{col}' — filled {data[col].isnull().sum()} missing values with mean ({mean_val:.2f})")

# --- Categorical columns: Mode Imputation ---
categorical_cols = ['Season', 'Station']

for col in categorical_cols:
    if col in data.columns and data[col].isnull().sum() > 0:
        mode_val = data[col].mode()[0]
        data[col] = data[col].fillna(mode_val)
        print(f"   ✔ '{col}' — filled missing values with mode ('{mode_val}')")

print("\n   Missing values after imputation:")
print(data.isnull().sum())


# ──────────────────────────────────────────────
# SECTION 3: OUTLIER DETECTION (IQR METHOD)
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("  STEP 3: OUTLIER DETECTION (IQR Method)")
print("=" * 55)

def detect_outliers_iqr(df, column):
    """Detect outliers in a column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

for col in ['Rainfall', 'Discharge']:
    if col in data.columns:
        outliers, lb, ub = detect_outliers_iqr(data, col)
        print(f"\n   Column: '{col}'")
        print(f"   Lower Bound: {lb:.2f}  |  Upper Bound: {ub:.2f}")
        print(f"   Outliers detected: {len(outliers)} rows")
        if not outliers.empty:
            print(outliers[[col]].head())

print("\n   ⚠ Note: Hydrological outliers (floods, storms) are retained as")
print("   they represent real environmental events, not data errors.")


# ──────────────────────────────────────────────
# SECTION 4: DATA TRANSFORMATIONS
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("  STEP 4: DATA TRANSFORMATIONS")
print("=" * 55)

# --- 4a. Standardization (Z-score Scaling) ---
print("\n   4a. Standardization (mean=0, std=1)")

cols_to_scale = [c for c in ['Rainfall', 'Discharge'] if c in data.columns]
scaler = StandardScaler()
data[cols_to_scale] = scaler.fit_transform(data[cols_to_scale])

print(f"   ✔ Scaled columns: {cols_to_scale}")
print(data[cols_to_scale].describe().round(3))

# --- 4b. One-Hot Encoding for Categorical Variables ---
print("\n   4b. One-Hot Encoding for 'Season'")

if 'Season' in data.columns:
    data = pd.get_dummies(data, columns=['Season'], prefix='Season')
    new_cols = [c for c in data.columns if c.startswith('Season_')]
    print(f"   ✔ New dummy columns created: {new_cols}")


# ──────────────────────────────────────────────
# SECTION 5: FEATURE ENGINEERING
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("  STEP 5: FEATURE ENGINEERING")
print("=" * 55)

# --- Feature 1: Rainfall Intensity (mm per hour) ---
# Derived from daily rainfall divided by 24 hours
if 'Rainfall' in data.columns:
    data['Rainfall_Intensity'] = data['Rainfall'] / 24
    print("\n   ✔ Feature created: 'Rainfall_Intensity' = Rainfall / 24")
    print("     (Converts daily rainfall total into hourly intensity)")

# --- Feature 2: Discharge-to-Rainfall Ratio ---
# Measures how much river discharge is produced per unit of rainfall
if 'Discharge' in data.columns and 'Rainfall' in data.columns:
    data['Discharge_Rainfall_Ratio'] = data['Discharge'] / (data['Rainfall'] + 1)
    print("\n   ✔ Feature created: 'Discharge_Rainfall_Ratio' = Discharge / (Rainfall + 1)")
    print("     (Quantifies river response to precipitation; +1 avoids division by zero)")

print("\n   New features preview:")
feat_cols = ['Rainfall_Intensity', 'Discharge_Rainfall_Ratio']
print(data[[c for c in feat_cols if c in data.columns]].head())


# ──────────────────────────────────────────────
# SECTION 6: SAVE PROCESSED DATASET
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("  STEP 6: SAVING OUTPUT")
print("=" * 55)

os.makedirs("outputs", exist_ok=True)
data.to_csv(OUTPUT_PATH, index=False)

print(f"\n   ✅ Processed dataset saved to: {OUTPUT_PATH}")
print(f"   Final shape: {data.shape[0]} rows × {data.shape[1]} columns")
print("\n" + "=" * 55)
print("  PIPELINE COMPLETE")
print("=" * 55)
