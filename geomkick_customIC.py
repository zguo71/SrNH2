orbitals = [24, 25, 26, 27] 
cores = 1 # number of processor cores to use
geomtest = False #If true, alvagadro file will be generated for each geometry, but cfour will not be run
A2B = 1.8897259886
use_custom_internal_coords = True


# module import
import numpy as np
import os
import subprocess
import sys
import time
print("\nModules imported\n")

# obtain location of cart2int.x
def get_COL_dir() -> str:
    '''returns the directory of COLUMBUS'''
    rv = subprocess.check_output(['echo $COLUMBUS'], shell = True, text = True)
    directory = rv.split('\n')[0]
    if directory:
        if directory[-1] == '/':
            return directory[:-1]
        else:
            return directory
    else:
        return '/home/cavanes1/C/columbus-v7.2/Columbus'

cart2int_loc = get_COL_dir()

# CFOUR input ("ZMAT")
ZMATtxt = """SrNH2
{GM}
*CFOUR(CALC=CCSD
UNIT=BOHR
EXCITE=EOMEA
BASIC=SPECIAL
RELATIVISTIC=X2C1E
DROPMO=1>10
COORD=CARTESIAN
EOMFOLLOW=OVERLAP
ESTATE_LOCK=OFF
SCF_CONV=9
CC_CONV=9
ESTATE_CONV=7
SCF_DAMPING=500
SCF_EXPSTART=10
CHARGE=1
MEM={GB}
MEM_UNIT=GB)

SR:PWCVTZ-X2C
N:PVTZ_X2C
H:PVTZ-X2C
H:PVTZ-X2C

%excite*
1
1
1  0  {ORB}  0  1.0


"""

# basis sets for CFOUR, in "GENBAS" file
GENBAStxt = """N:PVTZ_X2C
Recontracted for X2C

  4
    0    1    2    3
    4    3    2    1
   10    5    2    1

  11420.000000   1712.000000    389.300000    110.000000     35.570000
     12.540000      4.644000      1.293000      0.511800      0.178700

   0.00014981   0.00067879  0.0000000  0.0000000
   0.00094949   0.00428582  0.0000000  0.0000000
   0.00471218   0.02113965  0.0000000  0.0000000
   0.01866655   0.08119205  0.0000000  0.0000000
   0.05750170   0.23343514  0.0000000  0.0000000
   0.13221853   0.43331673  0.0000000  0.0000000
   0.17214529   0.34691073  0.0000000  0.0000000
  -0.15265688   0.04115865  1.0000000  0.0000000
  -0.59994849  -0.00848331  0.0000000  0.0000000
  -0.38670047   0.00237753  0.0000000  1.0000000

     26.630000      5.948000      1.742000      0.555000      0.172500

   0.01473672  0.0000000  0.0000000
   0.09183366  0.0000000  0.0000000
   0.29868477  0.0000000  0.0000000
   0.49837524  1.0000000  0.0000000
   0.33711092  0.0000000  1.0000000

      1.654000      0.469000

 1.0000000  0.0000000
 0.0000000  1.0000000

      1.093000

 1.0000000

N:PVTZ-X2C
recontracted with X2C

  4
    0    1    2    3    4    5    6    7
    4    3    2    1    0    0    0    0
   10    5    2    1    0    0    0    0

      11420.00000000       1712.00000000        389.30000000        110.00000000         35.57000000
         12.54000000          4.64400000          1.29300000          0.51180000          0.17870000

   0.00014981   0.00067879   0.00000000   0.00000000
   0.00094949   0.00428582   0.00000000   0.00000000
   0.00471218   0.02113965   0.00000000   0.00000000
   0.01866655   0.08119205   0.00000000   0.00000000
   0.05750170   0.23343514   0.00000000   0.00000000
   0.13221853   0.43331673   0.00000000   0.00000000
   0.17214529   0.34691073   0.00000000   0.00000000
  -0.15265688   0.04115865   1.00000000   0.00000000
  -0.59994849  -0.00848331   0.00000000   0.00000000
  -0.38670047   0.00237753   0.00000000   1.00000000

         26.63000000          5.94800000          1.74200000          0.55500000          0.17250000

   0.01473672   0.00000000   0.00000000
   0.09183366   0.00000000   0.00000000
   0.29868477   0.00000000   0.00000000
   0.49837524   1.00000000   0.00000000
   0.33711092   0.00000000   1.00000000

          1.65400000          0.46900000

   1.00000000   0.00000000
   0.00000000   1.00000000

          1.09300000

   1.00000000

H:PVTZ-X2C
recontracted with X2C

  3
    0    1    2    3    4    5    6    7
    3    2    1    0    0    0    0    0
    5    2    1    0    0    0    0    0

         33.87000000          5.09500000          1.15900000          0.32580000          0.10270000

   0.00607729   0.00000000   0.00000000
   0.04531797 	0.00000000   0.00000000
   0.20283562 	0.00000000   0.00000000
   0.50390186 	1.00000000   0.00000000
   0.38340398 	0.00000000   1.00000000

          1.40700000          0.38800000

   1.00000000   0.00000000
   0.00000000   1.00000000

          1.05700000

  1.000000000

SR:PWCVTZ-X2C
cc-pwCVTZ-X2C

  4
    0    1    2    3
    9    8    6    2
   30   22   17    2

8.268188D+07 1.933897D+07 5.618373D+06 1.803504D+06 6.292678D+05
2.346290D+05 9.268303D+04 3.848584D+04 1.669953D+04 7.533040D+03
3.516987D+03 1.692794D+03 8.370832D+02 4.239942D+02 2.191837D+02
1.146989D+02 5.838583D+01 3.114581D+01 1.664343D+01 8.610121D+00
4.518963D+00 2.355236D+00 1.078933D+00 1.073300D+00 5.495608D-01
2.648600D-01 2.221200D-01 7.236985D-02 3.682742D-02 1.778860D-02

4.700000D-05 -1.600000D-05 6.000000D-06 0.000000D+00 2.000000D-06 0.000000D+00 0.000000D+00
-1.000000D-06 0.000000D+00
6.600000D-05 -2.200000D-05 9.000000D-06 0.000000D+00 3.000000D-06 0.000000D+00 0.000000D+00
-1.000000D-06 0.000000D+00
1.750000D-04 -5.700000D-05 2.400000D-05 0.000000D+00 8.000000D-06 0.000000D+00 0.000000D+00
-2.000000D-06 0.000000D+00
3.390000D-04 -1.120000D-04 4.600000D-05 0.000000D+00 1.600000D-05 0.000000D+00 0.000000D+00
-4.000000D-06 0.000000D+00
7.250000D-04 -2.390000D-04 9.800000D-05 0.000000D+00 3.500000D-05 0.000000D+00 0.000000D+00
-9.000000D-06 0.000000D+00
1.468000D-03 -4.850000D-04 1.990000D-04 0.000000D+00 7.100000D-05 0.000000D+00 0.000000D+00
-1.800000D-05 0.000000D+00
3.059000D-03 -1.013000D-03 4.160000D-04 0.000000D+00 1.480000D-04 0.000000D+00 0.000000D+00
-3.800000D-05 0.000000D+00
6.370000D-03 -2.120000D-03 8.710000D-04 0.000000D+00 3.100000D-04 0.000000D+00 0.000000D+00
-8.000000D-05 0.000000D+00
1.344800D-02 -4.513000D-03 1.857000D-03 0.000000D+00 6.610000D-04 0.000000D+00 0.000000D+00
-1.710000D-04 0.000000D+00
2.828100D-02 -9.620000D-03 3.964000D-03 0.000000D+00 1.410000D-03 0.000000D+00 0.000000D+00
-3.650000D-04 0.000000D+00
5.837100D-02 -2.039000D-02 8.434000D-03 0.000000D+00 3.007000D-03 0.000000D+00 0.000000D+00
-7.800000D-04 0.000000D+00
1.142200D-01 -4.183400D-02 1.741100D-02 0.000000D+00 6.200000D-03 0.000000D+00 0.000000D+00
-1.606000D-03 0.000000D+00
2.003300D-01 -8.043000D-02 3.391800D-02 0.000000D+00 1.214100D-02 0.000000D+00 0.000000D+00
-3.152000D-03 0.000000D+00
2.857620D-01 -1.350870D-01 5.829200D-02 0.000000D+00 2.086300D-02 0.000000D+00 0.000000D+00
-5.404000D-03 0.000000D+00
2.812760D-01 -1.741750D-01 7.845600D-02 0.000000D+00 2.845800D-02 0.000000D+00 0.000000D+00
-7.412000D-03 0.000000D+00
1.474350D-01 -9.761000D-02 4.610400D-02 0.000000D+00 1.658200D-02 0.000000D+00 0.000000D+00
-4.266000D-03 0.000000D+00
2.524100D-02 2.048000D-01 -1.183720D-01 0.000000D+00 -4.403300D-02 0.000000D+00 0.000000D+00
1.139200D-02 0.000000D+00
-1.870000D-04 5.141550D-01 -3.937650D-01 0.000000D+00 -1.575300D-01 0.000000D+00 0.000000D+00
4.163800D-02 0.000000D+00
5.920000D-04 3.798970D-01 -3.930400D-01 0.000000D+00 -1.609770D-01 0.000000D+00 0.000000D+00
4.210200D-02 0.000000D+00
-3.210000D-04 8.152100D-02 1.516170D-01 0.000000D+00 6.938700D-02 0.000000D+00 0.000000D+00
-1.760600D-02 0.000000D+00
1.190000D-04 2.351000D-03 6.846920D-01 0.000000D+00 4.236950D-01 0.000000D+00 0.000000D+00
-1.205470D-01 0.000000D+00
-8.300000D-05 1.595000D-03 4.352330D-01 0.000000D+00 4.702430D-01 0.000000D+00 0.000000D+00
-1.391700D-01 0.000000D+00
4.200000D-05 -4.920000D-04 4.784200D-02 0.000000D+00 -2.172280D-01 0.000000D+00 0.000000D+00
7.685600D-02 0.000000D+00
0.000000D+00 0.000000D+00 0.000000D+00 1.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00
0.000000D+00 0.000000D+00
-2.100000D-05 1.740000D-04 -2.533000D-03 0.000000D+00 -7.435530D-01 0.000000D+00 0.000000D+00
2.952140D-01 0.000000D+00
9.000000D-06 -9.500000D-05 1.483000D-03 0.000000D+00 -3.649930D-01 0.000000D+00 0.000000D+00
3.106760D-01 0.000000D+00
0.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00 1.000000D+00 0.000000D+00
0.000000D+00 0.000000D+00
-3.000000D-06 3.100000D-05 -3.180000D-04 0.000000D+00 -1.421300D-02 0.000000D+00 1.000000D+00
-3.679380D-01 0.000000D+00
2.000000D-06 -2.300000D-05 2.330000D-04 0.000000D+00 5.563000D-03 0.000000D+00 0.000000D+00
-6.187540D-01 0.000000D+00
-1.000000D-06 7.000000D-06 -6.800000D-05 0.000000D+00 -1.288000D-03 0.000000D+00 0.000000D+00
-2.217040D-01 1.000000D+00

4.614013D+05 6.805891D+04 1.538283D+04 4.524101D+03 1.594390D+03
6.355255D+02 2.761773D+02 1.277731D+02 6.167574D+01 3.070521D+01
1.544690D+01 7.908714D+00 4.066445D+00 2.100629D+00 1.107800D+00
1.041362D+00 5.041130D-01 2.434200D-01 2.389502D-01 9.225950D-02
4.193749D-02 1.817317D-02

1.900000D-05 -8.000000D-06 0.000000D+00 3.000000D-06 0.000000D+00 0.000000D+00 -1.000000D-06
0.000000D+00
9.600000D-05 -4.000000D-05 0.000000D+00 1.300000D-05 0.000000D+00 0.000000D+00 -3.000000D-06
0.000000D+00
4.500000D-04 -1.890000D-04 0.000000D+00 6.100000D-05 0.000000D+00 0.000000D+00 -1.400000D-05
0.000000D+00
1.970000D-03 -8.290000D-04 0.000000D+00 2.660000D-04 0.000000D+00 0.000000D+00 -6.000000D-05
0.000000D+00
7.913000D-03 -3.354000D-03 0.000000D+00 1.077000D-03 0.000000D+00 0.000000D+00 -2.420000D-04
0.000000D+00
2.814000D-02 -1.205600D-02 0.000000D+00 3.879000D-03 0.000000D+00 0.000000D+00 -8.730000D-04
0.000000D+00
8.452000D-02 -3.723000D-02 0.000000D+00 1.201700D-02 0.000000D+00 0.000000D+00 -2.703000D-03
0.000000D+00
2.000030D-01 -9.165200D-02 0.000000D+00 2.979100D-02 0.000000D+00 0.000000D+00 -6.711000D-03
0.000000D+00
3.393690D-01 -1.652880D-01 0.000000D+00 5.420000D-02 0.000000D+00 0.000000D+00 -1.220500D-02
0.000000D+00
3.470220D-01 -1.657940D-01 0.000000D+00 5.424800D-02 0.000000D+00 0.000000D+00 -1.224200D-02
0.000000D+00
1.582620D-01 5.809700D-02 0.000000D+00 -3.017400D-02 0.000000D+00 0.000000D+00 7.083000D-03
0.000000D+00
2.132700D-02 3.836460D-01 0.000000D+00 -1.586830D-01 0.000000D+00 0.000000D+00 3.635200D-02
0.000000D+00
2.765000D-03 4.622430D-01 0.000000D+00 -2.240700D-01 0.000000D+00 0.000000D+00 5.274300D-02
0.000000D+00
-5.130000D-04 2.060330D-01 0.000000D+00 -5.961700D-02 0.000000D+00 0.000000D+00 1.173400D-02
0.000000D+00
0.000000D+00 0.000000D+00 1.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00
0.000000D+00
4.260000D-04 2.511800D-02 0.000000D+00 3.254470D-01 0.000000D+00 0.000000D+00 -8.585400D-02
0.000000D+00
-2.350000D-04 7.400000D-04 0.000000D+00 5.219990D-01 0.000000D+00 0.000000D+00 -1.517990D-01
0.000000D+00
0.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00 1.000000D+00 0.000000D+00 0.000000D+00
0.000000D+00
1.090000D-04 9.000000D-05 0.000000D+00 2.893780D-01 0.000000D+00 0.000000D+00 -1.333120D-01
0.000000D+00
-4.900000D-05 -5.400000D-05 0.000000D+00 3.522300D-02 0.000000D+00 1.000000D+00 2.134730D-01
0.000000D+00
2.600000D-05 3.000000D-06 0.000000D+00 -2.537000D-03 0.000000D+00 0.000000D+00 6.193410D-01
0.000000D+00
-8.000000D-06 -3.000000D-06 0.000000D+00 1.134000D-03 0.000000D+00 0.000000D+00 3.091160D-01
1.000000D+00

1.646140D+03 4.714884D+02 1.786339D+02 7.779537D+01 3.707308D+01
1.884276D+01 9.886786D+00 5.229314D+00 2.753991D+00 1.400831D+00
1.058400D+00 6.404601D-01 4.098100D-01 2.914567D-01 1.362140D-01
6.439238D-02 2.943358D-02

1.590000D-04 0.000000D+00 0.000000D+00 2.100000D-05 0.000000D+00 0.000000D+00
1.426000D-03 0.000000D+00 0.000000D+00 1.860000D-04 0.000000D+00 0.000000D+00
8.274000D-03 0.000000D+00 0.000000D+00 1.084000D-03 0.000000D+00 0.000000D+00
3.279600D-02 0.000000D+00 0.000000D+00 4.299000D-03 0.000000D+00 0.000000D+00
9.222300D-02 0.000000D+00 0.000000D+00 1.222400D-02 0.000000D+00 0.000000D+00
1.904360D-01 0.000000D+00 0.000000D+00 2.526300D-02 0.000000D+00 0.000000D+00
2.857570D-01 0.000000D+00 0.000000D+00 3.732400D-02 0.000000D+00 0.000000D+00
3.176700D-01 0.000000D+00 0.000000D+00 3.902200D-02 0.000000D+00 0.000000D+00
2.378750D-01 0.000000D+00 0.000000D+00 2.048800D-02 0.000000D+00 0.000000D+00
9.639300D-02 0.000000D+00 0.000000D+00 -5.097000D-02 0.000000D+00 0.000000D+00
0.000000D+00 1.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00
1.344300D-02 0.000000D+00 0.000000D+00 -1.606620D-01 0.000000D+00 0.000000D+00
0.000000D+00 0.000000D+00 1.000000D+00 0.000000D+00 0.000000D+00 0.000000D+00
-2.490000D-04 0.000000D+00 0.000000D+00 -2.239950D-01 0.000000D+00 0.000000D+00
3.420000D-04 0.000000D+00 0.000000D+00 -3.017470D-01 0.000000D+00 0.000000D+00
-1.530000D-04 0.000000D+00 0.000000D+00 -2.996960D-01 1.000000D+00 0.000000D+00
4.500000D-05 0.000000D+00 0.000000D+00 -2.890140D-01 0.000000D+00 1.000000D+00

6.395500D-01 1.847717D-01

1.000000D+00 0.000000D+00
0.000000D+00 1.000000D+00


"""

# equilibrium Cartesian geometry in units of Bohr radii (COLUMBUS format, "geom")
geomtxt = """ Sr   38.0    0.00000000    0.00000000   -0.68198419    0.00000000
 N     7.0    0.00000000    0.00000000    3.59387835   14.00307401
 H     1.0   -1.51059587    0.00000000    4.77508354    1.00782504
 H     1.0    1.51059587    0.00000000    4.77508354    1.00782504"""

# dummy Cartesian gradient in atomic units (COLUMBUS format, "cartgrd")
cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""

# cart2int input to convert internal to Cartesian coordinates ("cart2intin")
i2ctxt = """ &input
    calctype='int2cart'
 /"""

# cart2int input to convert Cartesian to internal coordinates ("cart2intin")
c2itxt = """ &input
    calctype='cart2int'
 /"""

# internal coordinate scheme (COLUMBUS format, "intcfl")
intcfltxt = """TEXAS
K                   STRE   1    1.        2.
K            1.     STRE   2    2.        3.
             1.     STRE        2.        4.
K            1.     BEND   3     3.        4.        2.
K            1.     OUT    4     1.        3.        4.        2.
K            1.     STRE   5    2.        3.
            -1.     STRE        2.        4.
K            1.     BEND   6     1.        4.        2.
            -1.     BEND         1.        3.        2.
  0.50E+01  0.50E+01  0.70E+01  0.50E+01  0.70E+01  0.10E+01"""

# SLURM job submission script
SLURMtxt = """#!/bin/bash
#SBATCH --job-name={name}
#SBATCH -p shared
#SBATCH -A dyarkon1
#SBATCH -N 1
#SBATCH -t 1:0:0
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
cp $workdir/GENBAS GENBAS

ml intel-mkl

xcfour

cd $workdir

/bin/rm -rf $tmpdir
"""

def filewrite(text: str, location: str):
    '''writes file to created directory
    text: text to write in the file
    location: path to the file to create'''
    f = open(location, "w")
    f.write(text)
    f.close()

def yesno(prompt: str = "") -> bool:
    '''yes or no input function that asks the user to type y or n, respectively
    prompt: text of the question to ask the user
    returns True if y and False if n'''
    print("\n")
    while True:
        x = input(prompt + " yes (y) or no (n)? ")
        if x == "y" or x == "n":
            return x == "y"
        else:
            print("\nYou did not input a 'y' or 'n', please try again.")

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

#Internal coordinate definittion
def internal_2_cartesian(coords, directory):
    IC1, IC2, IC3, IC4, IC5, IC6 = coords
    IC1 = IC1 * A2B
    IC2 = IC2 * A2B
    IC5 = IC5 * A2B
    N = np.array([0.0, 0.0, 0.0])

    # bond lengths
    NH1 = (IC2 + IC5) / 2
    NH2 = (IC2 - IC5) / 2
    SrN = IC1

    # place Hs
    HNH = IC3 / 2
    H1Y = NH1 * np.sin(HNH)
    H1Z = -NH1 * np.cos(HNH)
    H2Y = -NH2 * np.sin(HNH)
    H2Z = -NH2 * np.cos(HNH)
    H1 = np.array([0.0, H1Y, H1Z])
    H2 = np.array([0.0, H2Y, H2Z])

    # place Sr
    OOP = IC4
    SrX = np.sin(OOP) * SrN
    Zproj = np.sqrt(SrN**2 - SrX**2)
    bendangle = IC6
    SrZ = np.cos(bendangle) * Zproj
    SrY = np.sin(bendangle) * Zproj
    Sr = np.array([SrX, SrY, SrZ])

    return {
        'Sr': Sr,
        'N': N,
        'H1': H1,
        'H2': H2,
    }

def int_to_cart(intdisp = [0]*6, directory: str = "."):
    '''converts internal to Cartesian coordinates using COLUMBUS's cart2int.x
    intdisp: displacement in internal coordinates (defined by intcfl) from the reference geometry
        it is a list with 6 float elements, each corresponding to one of the 6 internal coordinates
        STRE (distance coordinates) are in Angstroms and all others (angular coordinates) are in radians
    directory: name of folder to work in for this geometry'''
    if use_custom_internal_coords:
        min1 = np.array([2.26268918, 1.43506504, 1.81432190, 0.0, 0.0, 0.0])
        newgeom = internal_2_cartesian(min1 + intdisp, directory)
        return [newgeom['Sr'], newgeom['N'], newgeom['H1'], newgeom['H2']]
    else:
        filewrite(geomtxt,    directory + "/geom")       # geom
        filewrite(cartgrdtxt, directory + "/cartgrd")    # dummy cartgrd
        filewrite(intcfltxt,  directory + "/intcfl")     # intcfl
        filewrite(i2ctxt,     directory + "/cart2intin") # cart2int input
        min1 = np.array([2.26268918, 1.43506504, 1.81432190, 0.0, 0.0, 0.0])
        intgeom = min1 + np.array(intdisp)
        partial_disp = np.zeros(len(intdisp))
        while True:
            for coord in range(len(intdisp)):
                if abs(intdisp[coord] - partial_disp[coord]) > 0.5:
                    partial_disp[coord] += 0.5*np.sign(intdisp[coord])
                else:
                    partial_disp[coord] = intdisp[coord]
            g = open(directory + '/intgeomch', "w")
            firstline = True
            for coord in (min1 + partial_disp):
                if not firstline:
                    g.write("\n")
                g.write(format(coord, "14.8f"))
                firstline = False
            g.close()
            rv = subprocess.run([cart2int_loc + "/cart2int.x"], cwd="./" + directory, capture_output=True)
            if rv.stdout.decode('utf8'):
                print(rv.stdout.decode('utf8'))
            filecheck(directory + "/geom.new")
            os.system("mv " + directory + "/geom.new " + directory + "/geom")
            if (partial_disp == intdisp).all():
                break
        filewrite(c2itxt, directory + "/cart2intin") # cart2int input
        rv = subprocess.run([cart2int_loc + "/cart2int.x"], cwd="./" + directory, capture_output=True)
        if rv.stdout.decode('utf8'):
            print(rv.stdout.decode('utf8'))
        int_geom_diff = np.array(getintcoord(directory)) - intgeom
        for coord in range(len(int_geom_diff)):
            if abs(int_geom_diff[coord]) > 0.000001:
                print("WARNING: Internal coordinate discrepancy of " + str(int_geom_diff[coord]) + " in coordinate " + str(coord + 1))
        g = open(directory + "/geom", "r")
        lines = g.readlines()
        g.close()
        newgeom = []
        for line in lines:
            newgeom.append([float(x) for x in line.split()[2:5]])
        return newgeom


def prepcalc(intdisp = [0]*6, directory: str = "TEST"):
    '''prepares CFOUR for each geometry
    intdisp: displacement in internal coordinates (defined by intcfl) from the reference geometry
        it is a list with 6 float elements, each corresponding to one of the 6 internal coordinates
        STRE (distance coordinates) are in Angstroms and all others (angular coordinates) are in radians
    directory: name of folder to work in for this geometry'''
    print("Preparing CFOUR input for " + directory)
    # if directory already exists, check if it is okay to overwrite it
    if os.path.isdir(directory):
        if yesno("There is already a directory called '{}', so it will now be deleted, is that OK?".format(directory)):
            os.system("rm -r " + directory)
        else:
            sys.exit("The program terminated because you chose not to overwrite the directory.")
    os.system("mkdir " + directory)
    # convert internal to Cartesian coordinates
    newgeom = int_to_cart(intdisp, directory)
    # create CFOUR input file ("ZMAT")
    atoms = ["SR", "N ", "H ", "H "]
    cartstr = ""
    for atom in range(len(atoms)):
        cartstr += atoms[atom]
        for coord in newgeom[atom]:
            cartstr += format(coord, "15.8f")
        cartstr += "\n"
    if not geomtest: # copy required files into new directory
        for orb in orbitals: # for each root
            subdir = directory + "/" + str(orb)
            os.system("mkdir " + subdir)
            filewrite(SLURMtxt.format(name = directory + str(orb), n = str(cores)), subdir + '/script.sh') # SLURM script
            filewrite(GENBAStxt, subdir + "/GENBAS") # GENBAS
            filewrite(ZMATtxt.format(GM = cartstr, GB = str(cores*3), ORB = str(orb)), subdir + '/ZMAT')
            # submit CFOUR job to SLURM
            rv = subprocess.run(["sbatch", "script.sh"], cwd="./" + subdir, capture_output=True)
            print(rv.stdout.decode('utf8'))
        #os.system("rm " +
        #          directory + "/bmatrix " +
        #          directory + "/bummer " +
        #          directory + "/cart2intin " +
        #          directory + "/cart2intls " +
        #          directory + "/cartgrd " +
        #          directory + "/geom " +
        #          directory + "/intcfl " +
        #          directory + "/intgeomch")
    else: # write .xyz file to view in Avogadro
        newgeom = np.array(newgeom)*0.529177211
        atoms = ["Ca", "N ", "H ", "H "]
        cartstr = "4\n\n"
        for atom in range(len(atoms)):
            cartstr += ' ' + atoms[atom] + ' '
            for coord in newgeom[atom]:
                cartstr += format(coord, "13.6f")
            cartstr += "\n"
        filewrite(cartstr, directory + '/geom.xyz')

# ----------------------------------------------------------------------------
#         main body of code
# ----------------------------------------------------------------------------
start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end   = int(sys.argv[2]) if len(sys.argv) > 2 else float("inf")

def fval(val):
    s = f"{abs(val*100):.0f}".replace('.', '')
    return f"n{s}" if val < 0 else s

def main(start, end):
    count = 0
    for i in [0.0]:
        for j in [0.0]:
            for k in [0.0]:
                for l in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
                    for m in [0.0]:
                        for n in [0.0]:
                            if ((abs(l) <= 0.1 and abs(n) <= 1.0) or
                                (abs(l) <= 0.4 and abs(n) <= 0.9) or
                                (abs(l) <= 0.6 and abs(n) <= 0.8) or
                                (abs(l) <= 0.7 and abs(n) <= 0.7) or
                                (abs(l) <= 0.9 and abs(n) <= 0.6) or
                                (abs(l) <= 1.0 and abs(n) <= 0.5)
                                  ):
                             count += 1
                             if count >= start and count <= end:
                                x = [i, j, k, l, m, n]
                                print(f"count = {count}  disp: {x}")
                                folder_name = f"{fval(i)}_{fval(j)}_{fval(k)}_{fval(l)}_{fval(m)}_{fval(n)}"
                                if os.path.exists(folder_name):
                                    print("Already calculated")
                                else:
                                    prepcalc(x, folder_name)

# manual
#main(start, end)

# automatic
last_submitted = start - 1 # last job that was submitted
while last_submitted <= end:
    # check how many jobs are running
    rv = subprocess.check_output(['squeue -u $USER'], shell = True, text = True)
    batch_size = 400 - len(rv.split('\n')) # how many jobs to run this time
    main(last_submitted + 1, last_submitted + batch_size//3) # run the jobs
    last_submitted += batch_size//3
    time.sleep(120) # wait for the submitted jobs to run
