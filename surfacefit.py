#input parameters
input_filename = 'input_xabc'
output_filename = 'fitted_output.txt'
ref_energy = [-3233.597872877419377, -3233.532946475688732, -3233.530968466364357, -3233.524213783323830] 
#ref_energy = [-732.93748280939246, -732.867103376558248, -732.864626241796600, -732.855458075144952] #CaNH2
polynomial_degree = 2

#module imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#reading data
df = pd.read_csv(input_filename, sep = r'\s+', header = None)
all_cols = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'G', 'A', 'B', 'C']
df.columns = all_cols
for j, E in enumerate(all_cols[-4:]):
    df['rel_' + E] = df[E] - ref_energy[j]
df.sort_values(by = [all_cols[-4]])
print(df)

#preparation for fitting
X = df[["c1", "c2", "c3", "c4", "c5", "c6"]]
poly = PolynomialFeatures(polynomial_degree, include_bias = False)
poly_features = poly.fit_transform(X)
terms = poly.get_feature_names_out()
print(terms)

df_out = df[['c1', 'c2', 'c3', 'c4', 'c5', 'c6']].copy()

#surface fitting
models = []
for j, E in enumerate(all_cols[-4:]):
    model = LinearRegression(fit_intercept=False)
    y = df["rel_" + E]
    df_out['energy' + E] = y
    model.fit(poly_features, y)
    refE = model.intercept_
    coeffs = model.coef_
    print("\n" + E)
    print("Reference energy: " + str(refE))
    print("Coefficients")
    print(coeffs)
    #root_mean_square
    poly_reg_y_predicted = model.predict(poly_features)
    df_out['fit' + E] = poly_reg_y_predicted
    df_out['difference' + E] = df_out['energy' + E] - df_out['fit' + E]
    poly_reg_rmse = np.sqrt(mean_squared_error(y, poly_reg_y_predicted))
    print("RMSE: " +  str(poly_reg_rmse))

    #output writing
    for i, term in enumerate(terms):
        print(term.rjust(10), format(coeffs[i], "9.5f"))
    #    header_lines = ['# Coefficients (degree_c1 degree_c2 ... degree_c6 coefficient):']

    powers = poly.powers_

    #for power, coef in zip(powers, coeffs):
    #    if abs(coef) > 1e-18:
    #        power_str = ' '.join(str(p) for p in power)
    #        header_lines.append(f"# {power_str} {coef:.10e}")

    #print out the intercept and RMS difference
    #header_lines.append(f"# Intercept (reference energy): {refE:.10e}")
    #header_lines.append(f"# RMS difference: {poly_reg_rmse:.10f}")
    header = (f"{'c1':>8}{'c2':>8}{'c3':>8}{'c4':>8}{'c5':>8}{'c6':>8}"
    f"{'energy X':>14}{'fit':>14}{'difference':>20}"
    f"{'energy A':>14}{'fit':>14}{'difference':>20}"
    f"{'energy B':>14}{'fit':>14}{'difference':>20}"
    f"{'energy C':>14}{'fit':>14}{'difference':>20}"
)
    #header = '\n'.join(header_lines)
    models.append(model)

#sorting based on coordinate value
df_out['sort_key'] = df_out['c1'] + df_out['c2'] + df_out['c3'] + df_out['c4'] + df_out['c5'] + df_out['c6']
df_out = df_out.sort_values(by='sort_key', ascending=False).drop(columns='sort_key')
#writing the output
#fmt = "%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f  %12.6f  %12.6f  %20.12f %12.6f  %12.6f  %20.12f  %12.6f  %12.6f  %20.12f  %12.6f  %12.6f  %20.12f"
fmt = "%7.2f"*6 + " %12.6f  %12.6f  %20.12f"*4
with open(output_filename, 'w') as f:
    f.write(header + '\n')
    for _, row in df_out.iterrows():
        f.write(fmt % tuple(row.values) + '\n')
