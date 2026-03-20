#import modules
import sys
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
print("\nModules loaded")

#getting user input of the parameters
polynomial_degree = 6
model_file = "model"
cfour_energy_file = "fitted_output.txt"
ht2wn = 219474.6

if len(sys.argv) > 4:
    rnge, step, x1, x2 = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
elif len(sys.argv) > 3:
    rnge, step, x1, x2 = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), 0
else:
    sys.exit("Not enough input variables, you must specify python view.py [range] [step] [coord1] [coord2 (optional)]")

spacing = rnge/step

#prepare the polynomial model
loaded_model = joblib.load(model_file)
print("\nModel loaded from file '" + model_file + "'")
def getsurfE(rel_int):
    rel_int = np.array(rel_int)
    relative_int = rel_int.reshape(1, -1)
    poly = PolynomialFeatures(polynomial_degree, include_bias = False)
    poly_features = poly.fit_transform(relative_int)
    output =  loaded_model.predict(poly_features)
    return output[0]

#get the cfour exact data
columns = ['c1','c2','c3','c4','c5','c6',
          'energy_X','fit_X','diff_X']
#           'energy_A','fit_A','diff_A',
#           'energy_B','fit_B','diff_B',
#           'energy_C','fit_C','diff_C']

with open(cfour_energy_file, 'r') as f:
    lines = f.readlines()

start_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("c1"):
        start_idx = i + 1
        break
if start_idx is None:
    raise ValueError("cannot fine line starting with c1")

data_lines = ''.join(lines[start_idx:])

df = pd.read_csv(StringIO(data_lines), delim_whitespace=True, names=columns)
print("\nCFOUR data loaded from " + cfour_energy_file)

def getcfourE(relative_int):
    df2 = df[(df['c1'] == relative_int[0]) & (df['c2'] == relative_int[1]) & (df['c3'] == relative_int[2]) &
        (df['c4'] == relative_int[3]) & (df['c5'] == relative_int[4]) & (df['c6'] == relative_int[5])] 
    val =  df2['energy_X'].iloc[0] 
    print(val)
    return val
#retriving data
coordcfour, coordfit, cfourE, fitE = [], [], [], []
rangelist = range(-step, step + 1)
step = step*2 + 1
for entry in rangelist:
    coordfit.append(round(entry*spacing, 5))
print()
for c in coordfit:
    intc = [0]*6 # create list with zeroes
    intc[x1 - 1] = c # displace first coordinate
    if x2 != 0: # if doing pairwise displacement
        intc[x2 - 1] = c # displace second coordinate
    fitE.append(getsurfE(intc))
    try:
        cfourE.append(getcfourE(intc))
        coordcfour.append(c)
        print("Identified CFOUR datum for coordinate value of " + str(c))
    except:
        print("No CFOUR data for " + str(c))
print("\nFinished retrieving data, now ready to plot")

#plot
plt.figure(figsize=(10,5))
plt.plot(coordfit, np.array(fitE) * ht2wn, label = "fit")
plt.plot(coordcfour, np.array(cfourE) * ht2wn, 'o', label = "cfour")
if x2 != 0:
    plt.title("Pairwise displacement in coords " + str(x1) + " and " + str(x2))
else:
    plt.title("Displacement in coordinate " + str(x1))
plt.xlabel("Value of coordinate")
plt.ylabel("Energy (cm-1)")
plt.savefig("16")
plt.close()
print("\nPlot saved to " + "16" + ".png")


