# Usage
# python crossing.py [energy gap threshold, cm-1] [energy upper bound, cm-1]

# Import modules
import numpy as np
import pandas as pd
import sys

# Important values and constants
tolerance = int(sys.argv[1]) if len(sys.argv) > 1 else 230 # in wavenumbers
E_lim = int(sys.argv[2]) if len(sys.argv) > 2 else 2000 #in wavenumbers
au2cm = 219474.63137
col_names = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'X', 'A', 'B', 'C']
ref_E = [-3233.597872877419377, -3233.532946475688732, -3233.530968466364357, -3233.524213783323830]  

# Calculate energy gaps
df = pd.read_csv('input_xabc', header = None, delim_whitespace=True, names = col_names)
df['XE1_diff'] = (df.iloc[:,7] - df.iloc[:,6]) * au2cm
df['E1E2_diff'] = (df.iloc[:,8] - df.iloc[:,7]) * au2cm
df['E2E3_diff'] = (df.iloc[:,9] - df.iloc[:,8]) * au2cm

#conversion
df['X_cm'] = (df['X'] - ref_E[0]) * au2cm
df['A_cm'] = (df['A'] - ref_E[1]) * au2cm
df['B_cm'] = (df['B'] - ref_E[2]) * au2cm
df['C_cm'] = (df['C'] - ref_E[3]) * au2cm

#filtering
mask1 = np.isclose(df['XE1_diff'], 0, atol=tolerance)
mask2 = np.isclose(df['E1E2_diff'], 0, atol=tolerance)
mask3 = np.isclose(df['E2E3_diff'], 0, atol=tolerance)
mask4 = np.isclose(df['X_cm'], 0, atol=E_lim)
mask5 = np.isclose(df['A_cm'], 0, atol=E_lim)
mask6 = np.isclose(df['B_cm'], 0, atol=E_lim)
mask7 = np.isclose(df['C_cm'], 0, atol=E_lim)
diff_mask = mask1 | mask2 | mask3
Emask     = mask4 | mask5 | mask6 | mask7
mask      = diff_mask & Emask

# Print out the data we want
out = df.loc[mask, ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'X', 'A', 'B', 'C', 'XE1_diff', 'E1E2_diff', 'E2E3_diff', 'X_cm', 'A_cm', 'B_cm', 'C_cm']]
out_cm = out[['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'X_cm', 'A_cm', 'B_cm', 'C_cm', 'XE1_diff', 'E1E2_diff', 'E2E3_diff']]
print(out_cm)
