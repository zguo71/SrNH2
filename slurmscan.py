# Usage: 'python runpolyreg.py'         to make new input,
#        'python runpolyreg.py [input]' to continue from existing data
# Prerequisite: You must have Intel modules loaded
order = 4 # highest order of fitting polynomial
all_coords = False # explicity print all coordinates, even if unchanging
symmetrize = True # automatically generate symmetry-equivalent data

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
    directory: path to directory containing intgeomch
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
dirs = [ f.name for f in os.scandir("./") if f.is_dir() ]
for directory in dirs:
    print(directory)
    subdirs = [ int(f.name) for f in os.scandir("./" + directory) if f.is_dir() ]
    orbs = sorted(subdirs)
    for orb in orbs:
        SLURM_files = [ f.name for f in os.scandir(directory + "/" +str(orb)) if (f.is_file() and ("slurm-" in f.name)) ]
        SLURM_nums = [ int(filename[6:-4]) for filename in SLURM_files ]
        SLURM_nums.sort(reverse = True)
        if SLURM_nums == []:
            print("EMPTY")
