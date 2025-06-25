import pandas as pd
import numpy as np
from io import StringIO

# input parameters
input_file = 'fitted_output.txt'
hartree_to_wavenumber = 219474.63137
states = ['X', 'A', 'B', 'C']
ref_energy = {"X": 0,
              "A": 0,
              "B": 0,
              "C": 0}
thresholds = [2000, 1000, 500, 100]
error_bins = [0, 1, 10, 20, 50, 100, 500, 1000]

# read input fiels
with open(input_file, 'r') as f:
    lines = f.readlines()

start_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("c1"):
        start_idx = i + 1
        break
if start_idx is None:
    raise ValueError("cannot fine line starting with c1")

data_lines = ''.join(lines[start_idx:])

# Column names for fitted_output.txt
columns = ['c1','c2','c3','c4','c5','c6',
           'energy_X','fit_X','diff_X',
           'energy_A','fit_A','diff_A',
           'energy_B','fit_B','diff_B',
           'energy_C','fit_C','diff_C']
df = pd.read_csv(StringIO(data_lines), delim_whitespace=True, names=columns)

# Analysis for all of the states
results = {}
for state in states:
    e_col = f'energy_{state}'  # energy_X, energy_A, energy_B, energy_C
    f_col = f'fit_{state}'

    sub_df = df[['c1','c2','c3','c4','c5','c6', e_col, f_col]].copy()
    sub_df['error'] = df[f'diff_{state}']
    sub_df['error_cm'] = sub_df['error'] * hartree_to_wavenumber
    sub_df['rel_E'] = df[f'energy_{state}']
    sub_df['rel_E_cm'] = sub_df['rel_E'] * hartree_to_wavenumber

    # histogram analysis using the error calculated in wavenumber
    hist_df = (
        sub_df.groupby(pd.cut(sub_df['error_cm'].abs(), error_bins, right=True))
        .count()
        .reindex(pd.IntervalIndex.from_breaks(error_bins, closed='right'), fill_value=0)
    )

    #print(f"\n========== Histogram for State {state} ==========")
    #print(hist_df.to_string())


    # All rmse
    rmse_all = np.sqrt(np.mean(sub_df['error_cm']**2))

    # RMSE for each threshold
    rmse_dict = {}
    for t in thresholds:
        subset = sub_df[sub_df['rel_E_cm'] < t]
        if not subset.empty:
            rmse_dict[t] = np.sqrt(np.mean(subset['error_cm']**2))
        else:
            rmse_dict[t] = np.nan

    # histogram analysis on the distribution of errors
    hist = (
        sub_df.groupby(pd.cut(sub_df['error_cm'].abs(), error_bins, right=False))
        .size()
        .reindex(pd.IntervalIndex.from_breaks(error_bins, closed='left'), fill_value=0)
        .tolist()
    )

    # save the results
    results[state] = {
        'rmse': rmse_all,
        'rmse_by_threshold': rmse_dict,
        'histogram': hist,
        'table': sub_df[['c1','c2','c3','c4','c5','c6','rel_E_cm','error_cm']]
    }

    sub_df = sub_df.sort_values(by='error', key=abs, ascending = False)
    print(f"\n\n\n[{state}] rel_E_cm range: {sub_df['rel_E_cm'].min():.2f} – {sub_df['rel_E_cm'].max():.2f} cm⁻¹")
    print(f"\n========== Largest Errors for State {state} ==========")
    print(sub_df[['c1','c2','c3','c4','c5','c6','rel_E_cm','error_cm']].head(50).to_string(index=False))
    print(f"\n========== Smallest Errors for State {state} ==========")
    print(sub_df[['c1','c2','c3','c4','c5','c6','rel_E_cm','error_cm']].tail(50).to_string(index=False))

# Print out the results
for state in states:
    res = results[state]
    print(f"\n========== State {state} ==========")
    print(f"Global RMSE: {res['rmse']:.3f} cm⁻¹")
    for t in thresholds:
        v = res['rmse_by_threshold'][t]
        print(f"RMSE for rel_E_cm < {t:4d} cm⁻¹: {v:.3f} cm⁻¹")
    print("Error histogram (abs cm⁻¹ bins: 0–1–10–20–50–100–500–1000):")
    print(res['histogram'])

