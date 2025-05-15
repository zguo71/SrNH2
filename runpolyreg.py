# Usage: 'python runpolyreg.py'         to make new input,
#        'python runpolyreg.py [input]' to continue from existing data
# Prerequisite: You must have Intel modules loaded
order = 4 # highest order of fitting polynomial
all_coords = False # explicity print all coordinates, even if unchanging
symmetrize = False # automatically generate symmetry-equivalent data

# import modules
import os
import numpy as np
import sys
print("\nModules imported")

def filecheck(fl: str):
    '''checks for the presence of a file
    fl: path to the file to check
    quits the program with an error if the file is not present'''
    if not os.path.isfile(fl):
        sys.exit(fl + " is required, but is not present")

def getintcoord(directory: str):
    '''retrieve internal coordinate geometry
    directory: path to directory containing intgeom
    returns internal coordinate geometry (defined by intcfl)
        it is a list with 6 float elements, each corresponding to one of the 6 internal coordinates
        STRE (distance coordinates) are in Angstroms and all others (angular coordinates) are in radians'''
    filecheck(directory + "/intgeom")
    f = open(directory + "/intgeom", "r")
    lines = f.readlines()
    f.close()
    intgeom = []
    for line in lines:
        intgeom.append(float(line))
    return intgeom

def getlatestSLURM(directory: str) -> str:
    '''retrieve path of latest-generated SLURM output file
    directory: path to directory containing SLURM files'''
    SLURM_files = [ f.name for f in os.scandir(directory) if (f.is_file() and ("slurm-" in f.name)) ]
    SLURM_nums = [ int(filename[6:-4]) for filename in SLURM_files ]
    SLURM_nums.sort(reverse = True)
    print(SLURM_nums)
    print(SLURM_nums[0])
    last_SLURM = "slurm-" + str(SLURM_nums[0]) + ".out"
    return directory + "/" + last_SLURM

def getener(directory: str) -> list:
    '''retrieves energies from a completed CFOUR calculation
    directory: path to directory containing CFOUR calculation
    returns energies as strings in a list'''
    f = open(getlatestSLURM(directory), "r")
    lines = f.readlines()
    f.close()
    # maybe insert a check here that the calculation converged
    eners = []
    for line in lines:
        if "Total EOMEA-CCSD electronic energy" in line:
            eners.append(line.split()[-2])
    return eners

# ----------------------------------------------------------------------------
#         main body of code
# ----------------------------------------------------------------------------
min1 = np.array([2.26268918, 1.43506504, 1.81432190, 0.0, 0.0, 0.0]) # internal coordinate geom of ground state minimum of SrNH2

# for each directory, get the geometry and CFOUR result energy
intgeoms = []
eners = []
dirs = [ f.name for f in os.scandir("./") if f.is_dir() ]
for directory in dirs:
    print(f"Processing folder: {directory}")
    int_c = getintcoord(directory)
    E = getener(directory)
    intgeoms.append(int_c)
    eners.append(E)
    if symmetrize:
        # b1 symmetrization
        if int_c[3] != 0:
            sym_c = int_c.copy()
            sym_c[3] = -1*int_c[3]
            intgeoms.append(sym_c)
            eners.append(E)
        # b2 symmetrization
        if int_c[4] != 0 or int_c[5] != 0:
            sym_c = int_c.copy()
            sym_c[4], sym_c[5] = -1*int_c[4], -1*int_c[5]
            intgeoms.append(sym_c)
            eners.append(E)
        # b1 and b2 symmetrization
        if int_c[3] != 0 and (int_c[4] != 0 or int_c[5] != 0):
            sym_c = int_c.copy()
            sym_c[3], sym_c[4], sym_c[5] = -1*int_c[3], -1*int_c[4], -1*int_c[5]
            intgeoms.append(sym_c)
            eners.append(E)
intgeoms = np.array(intgeoms)

# determine which coordinates differ between calculations
# i.e., don't use unchanging internal coordinates in the fit
diff_coords = []
for coord in range(np.shape(intgeoms)[1]):
    rounded = np.round(intgeoms[:, coord], 7)
    if all_coords or len(np.unique(rounded)) != 1:
    #if all_coords or len(np.unique(intgeoms[:, coord])) != 1:
        diff_coords.append(coord)

# read already existing data
nOldPts = 0
lines = []
if len(sys.argv) > 1:
    print("Reading " + sys.argv[1])
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    nOldPts = len(lines) - 4
    print("Renaming " + sys.argv[1] + " to oldinput")
    os.system("mv "   + sys.argv[1] +    " oldinput")
# create input file for polyreg
npoints = len(intgeoms)
f = open("input", "w")
f.write(str(order)             + "\n") # maximum polynomial order
f.write(str(nOldPts + npoints) + "\n") # number of points
f.write(str(len(diff_coords))  + "\n") # number of fitted coordinates
f.write("1.0")                         # energy conversion factor
# re-add already existing data
if len(sys.argv) > 1:
    f.write("\n")
    for line in lines[4:]:
        f.write(line)
# add new data
for point in range(npoints): # for each geometry
    displacement = intgeoms[point] - min1
    f.write("\n")
    for coord in diff_coords: # write each coordinate
        f.write(format(displacement[coord], "5.2f") + '   ') # 'displacement/0.529177211' to convert Angstroms to Bohr radii
    for energy in eners[point]: # write energy
        f.write("   " + energy)
f.close()
print("\npolyreg input file written, now running polyreg")

# run polyreg
os.system("xpolyreg < input > out")
