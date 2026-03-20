# This is a script to test surface fitting behavior of a diatomic molecule
# at different scales for the purpose of better understanding the procedure
# for obtaining vibrational frequencies of a surface numerically.

cores = 1 # number of processor cores to use
run_CFOUR = True # set to False if you don't want to rerun CFOUR and data is already there

# Module imports
import numpy as np
import os
import subprocess
import time
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# constants
equil = 0.914122680207296 # equilibrium H-F distance in Angstroms
ref_energy = -100.344894364 # energy at equilibrium geometry
ht2cm = 219474.63137 # wavenumbers per Hartree

# CFOUR input file; GM is H-F distance in Angstroms
ZMATtxt = """HF
F
H 1 R

R={GM}

*CFOUR(CALC=CCSD
BASIS=PVTZ)

"""

# SLURM job submission script
SLURMtxt = """#!/bin/bash
#SBATCH --job-name={name}
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -t 0:5:0
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={n}

export OMP_NUM_THREADS={n}
export MKL_NUM_THREADS={n}
export PATH=$codedir:$PATH
export tmpdir=/tmp/$SLURM_JOBID
export workdir=$PWD
mkdir $tmpdir
cd $tmpdir
cp $workdir/ZMAT ZMAT

ml intel-mkl

xcfour

cd $workdir

/bin/rm -rf $tmpdir
rm script.sh ZMAT
"""

def filewrite(text: str, location: str):
    '''writes file to created directory
    text: text to write in the file
    location: path to the file to create'''
    f = open(location, "w")
    f.write(text)
    f.close()

def dir_namer(num: float) -> str:
    '''creates an appropriate directory name for a given number
    num: a floating point number (in this case the displacement H-F distance)'''
    precision = 3
    dir_name = format(num, "." + str(precision) + "f")[-precision:]
    if num < -0.0000001:
        dir_name = "n" + dir_name
    return dir_name

def prepcalc(bond_length: float = equil, directory: str = "TEST"):
    '''prepares CFOUR for each geometry
    bond_length: length of the bond between the two atoms in Angstroms
    directory: name of folder to work in for this geometry'''
    # if directory already exists, delete it
    if os.path.isdir(directory):
        print('Deleting ./' + directory + ' (already exists)', "   ", end="")
        os.system("rm -r " + directory)
    os.system("mkdir " + directory)
    # prepare CFOUR input
    print("Preparing CFOUR input for " + directory, "   ", end="")
    filewrite(SLURMtxt.format(name = directory, n = str(cores)), directory + '/script.sh') # SLURM script
    filewrite(ZMATtxt.format(GM = bond_length), directory + '/ZMAT') # create CFOUR input file ("ZMAT")
    # submit CFOUR job to SLURM
    rv = subprocess.run(["sbatch", "script.sh"], cwd="./" + directory, capture_output=True)
    print(rv.stdout.decode('utf8'), end="")

def getener(directory: str) -> tuple:
    '''retrieves energy and bond distance from a completed CFOUR calculation
    directory: path to directory containing CFOUR calculation
    returns bond distance and energy as floats (in a tuple?)'''
    with open(directory + "/" + os.listdir(directory)[0], "r") as f:
        lines = f.readlines()
    # maybe insert a check here that the calculation converged
    R, ener = 0, 0
    if "final" in lines[-2]:
        ener = float(lines[-2].split()[-2])
    for line in lines:
        if "R=" in line:
            R = float(line[2:])
            continue
    if R == 0 or ener == 0:
        sys.exit("ERROR: Could not obtain R and/or energy from " + directory)
    return R, ener

def fit_surf(df, polynomial_degree: int = 2, fit_int: bool = False):
    '''Perform surface fitting using scikit-learn'''
    # preparation for fitting
    x = df[["rel_R"]]
    poly = PolynomialFeatures(polynomial_degree, include_bias = False)
    poly_features = poly.fit_transform(x)
    terms = poly.get_feature_names_out()
    #print("\nTerms: ", terms)
    df_out = df.copy()
    
    # surface fitting
    model = LinearRegression(fit_intercept = fit_int)
    y = df["rel_cm"]
    model.fit(poly_features, y)
    intercept = model.intercept_
    coeffs = model.coef_
    #print("\nIntercept = " + str(intercept))
    #print("\nCoefficients: ", coeffs)
    
    # root_mean_square
    poly_reg_y_predicted = model.predict(poly_features)
    df_out['fit'] = poly_reg_y_predicted
    df_out['difference'] = df_out['rel_cm'] - df_out['fit']
    poly_reg_rmse = np.sqrt(mean_squared_error(y, poly_reg_y_predicted))

    # output writing
    print(f"\nResults of surface fitting (order = {polynomial_degree}, fit_int = {fit_int}):")
    print("\nRMSE = " +  str(poly_reg_rmse) + " cm^-1")
    print("\n Intercept " + format(intercept, "11.2f") + " cm^-1")
    for i, term in enumerate(terms):
        print(term.rjust(10), format(coeffs[i], "11.2f") + " cm^-1")
    print()

    return df_out

# ----------------------------------------------------------------------------
#                       main body of code
# ----------------------------------------------------------------------------

if run_CFOUR:
    # run CFOUR for all geometries
    for displacement in np.arange(-0.1, 0.1, 0.01):
        prepcalc(equil + displacement, dir_namer(displacement))

alldistances = [directory for directory in os.listdir("./") if os.path.isdir(directory)]
total_jobs = len(alldistances)

if run_CFOUR:
    # wait until jobs finish
    wait_time = 5 #seconds
    elapsed = 0
    running = True
    while running:
        time.sleep(wait_time)
        elapsed += wait_time
        print("\nChecking status," + format(elapsed, "3d") + "s elapsed...   ", end="")
        finished = 0
        for distance in alldistances:
            allfls = os.listdir(distance)
            if len(allfls) == 1:
                finished += 1
        if finished == total_jobs:
            running = False
            print("All jobs complete")
        else:
            print(str(finished) + " of " + str(total_jobs) + " jobs complete", end="")

# read CFOUR data
CFOUR_data = []
for distance in alldistances:
    CFOUR_data.append(getener(distance))
Rs, eners = zip(*CFOUR_data)
Rs, eners = np.array(Rs), np.array(eners)
df = pd.DataFrame({'directory': alldistances,
    'R': Rs,
    'rel_R': Rs - equil,
    'E': eners,
    'rel_E': eners - ref_energy,
    'rel_cm': (eners - ref_energy)*ht2cm})
df = df.sort_values("R")
print("\nCFOUR results obtained from completed SLURM files:\n")
print(df)

# surface fitting
for i in range(2, 10 + 1, 2):
    df_out = fit_surf(df, polynomial_degree = i, fit_int = True)
    with open(str(i) + ".txt", "w") as f:
        f.write(str(df_out))
