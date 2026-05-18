# generate_sample_data.py
# ─────────────────────────────────────────────────────────────────
# Run this script ONLY if you don't have the Kaggle dataset yet.
# It creates a realistic sample CSV with ~150 rows so you can test
# the preprocessing pipeline immediately.
#
# Usage:  python generate_sample_data.py
# Output: data/rainfall_discharge_dataset.csv
# ─────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd

np.random.seed(42)
N = 150  # number of observations

stations = ['Brahmaputra_G1', 'Brahmaputra_G2', 'Barak_G1', 'Subansiri_G1']
seasons  = ['Monsoon', 'Winter', 'Summer', 'Post-Monsoon']

data = pd.DataFrame({
    'Date':          pd.date_range(start='2020-01-01', periods=N, freq='D').strftime('%Y-%m-%d'),
    'Station':       np.random.choice(stations, N),
    'Season':        np.random.choice(seasons, N, p=[0.45, 0.15, 0.20, 0.20]),
    'Rainfall':      np.round(np.random.exponential(scale=12, size=N), 2),
    'Discharge':     np.round(np.random.normal(loc=350, scale=120, size=N).clip(10), 2),
    'Temperature':   np.round(np.random.normal(loc=27, scale=6, size=N), 1),
    'Soil_Moisture': np.round(np.random.uniform(20, 80, size=N), 1),
})

# Inject a few extreme values (simulated flood events)
data.loc[np.random.choice(N, 5, replace=False), 'Rainfall']  = np.round(np.random.uniform(120, 200, 5), 2)
data.loc[np.random.choice(N, 5, replace=False), 'Discharge'] = np.round(np.random.uniform(900, 1500, 5), 2)

# Inject ~10% missing values across numerical and categorical columns
for col, frac in [('Rainfall', 0.08), ('Soil_Moisture', 0.06),
                  ('Discharge', 0.05), ('Season', 0.04)]:
    idx = np.random.choice(N, int(N * frac), replace=False)
    data.loc[idx, col] = np.nan

os.makedirs("data", exist_ok=True)
data.to_csv(os.path.join("data", "rainfall_discharge_dataset.csv"), index=False)

print(f"✅ Sample dataset created: data/rainfall_discharge_dataset.csv")
print(f"   {N} rows × {data.shape[1]} columns")
print(f"   Missing values injected for realistic preprocessing practice.")
print(data.head())
