import pandas as pd
import numpy as np
from io import StringIO

input_file = 'fitted_output.txt'
ref_energy = -3233.597872877419377
threshold_wavenumber = 2000  
hartree_to_wavenumber = 219474.63137
with open(input_file, 'r') as f:
    lines = f.readlines()

start_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("c1"):
        start_idx = i
        break

data_lines = ''.join(lines[start_idx:])
col_names = ['c1','c2','c3','c4','c5','c6','energy','fit','difference']
col_widths = [8,8,8,8,8,8,12,12,20]


df = pd.read_fwf(StringIO(data_lines), names=col_names)

df[['c1','c2','c3','c4','c5','c6','energy','fit','difference']] = df[
    ['c1','c2','c3','c4','c5','c6','energy','fit','difference']
].apply(pd.to_numeric, errors='coerce')

df = df.dropna(subset=['energy', 'difference'])
#sort by error
df['error'] = (df['energy'] - df['fit'])
df['error_cm'] = df['error'] * hartree_to_wavenumber
df['rel_E'] = df['energy'] - ref_energy
df['rel_E_cm'] = df['rel_E'] * hartree_to_wavenumber
df = df.sort_values(by='error', key=abs, ascending = False)

#only analyze error of points < 2kcm-1
low_E_df = df[df['rel_E_cm'] < threshold_wavenumber]

low_e_rmse = np.sqrt(np.mean(low_E_df['error_cm']**2))
rmse = np.sqrt(np.mean(df['error_cm']**2))

#1000
onek_E_df = df[df['rel_E_cm'] < 1000]
onek_E_rmse = np.sqrt(np.mean(onek_E_df['error_cm']**2))

#500
halfk_E_df = df[df['rel_E_cm'] < 500]
halfk_E_rmse = np.sqrt(np.mean(halfk_E_df['error_cm']**2))

#100
onehund_E_df = df[df['rel_E_cm'] < 100]
onehund_E_rmse = np.sqrt(np.mean(onehund_E_df['error_cm']**2))
#count error bins
ranges = [0, 1, 10, 20, 50, 100, 500, 1000]
grouped = df.groupby(pd.cut(df.error_cm.abs(), ranges)).count()
print(grouped)
grouped_low_E = low_E_df.groupby(pd.cut(df.error_cm.abs(), ranges)).count()
print(grouped_low_E)

print("RMS of fitting error for points with < 2000 cm⁻¹ relative energy:")
print(f"RMS_low_E = {low_e_rmse:.3f} Wavenumbers")
print(f"RMS_1000_E = {onek_E_rmse:.3f} Wavenumbers")
print(f"RMS_500_E = {halfk_E_rmse:.3f} Wavenumbers")
print(f"RMS_100_E = {onehund_E_rmse:.3f} Wavenumbers")
print(f"RMSE = {rmse:.3f} Wavenumbers")
print(df[['c1','c2','c3','c4','c5','c6','rel_E_cm','error_cm']].head(5000).to_string(index=False))
print(df[['c1','c2','c3','c4','c5','c6','rel_E_cm','error_cm']].tail(5000).to_string(index=False))

