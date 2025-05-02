import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
input_filename = 'input'
output_filename = 'fitted_output.txt'
ref_energy = -3233.597872877419377
df = pd.read_csv(input_filename, sep = r'\s+', skiprows = 4, header = None)
df.columns = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'E']
df['rel_E'] = df['E'] - ref_energy
df.sort_values(by = ['E'])
X, y = df[["c1", "c2", "c3", "c4", "c5", "c6"]], df["rel_E"]
poly = PolynomialFeatures(degree = 6, include_bias = False)
poly_features = poly.fit_transform(X)
terms = poly.get_feature_names_out()
print(terms)
model = LinearRegression(fit_intercept=False)
model.fit(poly_features, y)
refE = model.intercept_
coeffs = model.coef_
print(refE)
print(coeffs)
poly_reg_y_predicted = model.predict(poly_features)
poly_reg_rmse = np.sqrt(mean_squared_error(y, poly_reg_y_predicted))
poly_reg_rmse
print("Coefficients")
print("Reference energy: " + str(refE))
for i, term in enumerate(terms):
    print(term.rjust(10), format(coeffs[i], "9.5f"))
    header_lines = ['# Coefficients (degree_c1 degree_c2 ... degree_c6 coefficient):']
powers = poly.powers_
for power, coef in zip(powers, coeffs):
    if abs(coef) > 1e-18:
        power_str = ' '.join(str(p) for p in power)
        header_lines.append(f"# {power_str} {coef:.10e}")

header_lines.append(f"# Intercept (reference energy): {refE:.10e}")
header_lines.append(f"# RMS difference: {poly_reg_rmse:.10f}")
header_lines.append(
    f"{'c1':>8}{'c2':>8}{'c3':>8}{'c4':>8}{'c5':>8}{'c6':>8}"
    f"{'energy':>12}{'fit':>12}{'difference':>20}"
)
header = '\n'.join(header_lines)

df_out = df[['c1', 'c2', 'c3', 'c4', 'c5', 'c6']].copy()
df_out['energy'] = y
df_out['fit'] = poly_reg_y_predicted
df_out['difference'] = df_out['energy'] - df_out['fit']

df_out['sort_key'] = df_out['c1'] + df_out['c2'] + df_out['c3'] + df_out['c4'] + df_out['c5'] + df_out['c6']
df_out = df_out.sort_values(by='sort_key', ascending=False).drop(columns='sort_key')

fmt = "%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f  %12.6f  %12.6f  %20.12f"

with open(output_filename, 'w') as f:
    f.write(header + '\n')
    for _, row in df_out.iterrows():
        f.write(fmt % tuple(row.values) + '\n')

    # Append RMS row
    rms_row = (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,  poly_reg_rmse)
    f.write(fmt % rms_row + '\n')
