import pandas as pd

coord_cols = ['c1','c2','c3','c4','c5','c6']
energy_cols2 = ['E1', 'E2', 'E3']
energy_cols1 = ['X']

df1 = pd.read_csv('input_x', delim_whitespace=True, header=None, low_memory=False)
df2 = pd.read_csv('input_excited', delim_whitespace=True, header=None, low_memory=False)

df1.columns = coord_cols + energy_cols1
df2.columns = coord_cols + energy_cols2

#df1_unique = df1.drop_duplicates(subset=coord_cols)
#df2_unique = df2.drop_duplicates(subset=coord_cols)

merged = pd.merge(df1, df2, on=coord_cols, how='inner')

final = merged[coord_cols + energy_cols2].astype(float) 

with open('input_xabc-3', 'w') as f:
    for row in final.itertuples(index=False):
        row_floats = list(map(float, row))
        coords = ''.join(f"{v: 8.2f}" for v in row[:6])
        energy = ''.join(f"{v:25.15f}" for v in row[6:])
        f.write(coords + energy + '\n')

