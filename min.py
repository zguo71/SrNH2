import pandas as pd

pd.set_option('display.precision', 15)

colnames = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'energy_X', 'energy_A', 'energy_B', 'energy_C']
df = pd.read_csv("input_xabc", delim_whitespace=True, names=colnames)

print(df[['energy_X', 'energy_A', 'energy_B', 'energy_C']].min())
