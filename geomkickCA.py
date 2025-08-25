orbitals = [16, 17, 18] 
cores = 1 # number of processor cores to use
geomtest = False #If true, alvagadro file will be generated for each geometry, but cfour will not be run

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
ZMATtxt = """CaNH2
{GM}
*CFOUR(CALC=CCSD
FCGRADNEW=NEW
EXCITE=EOMEA
BASIC=SPECIAL
DROPMO=1>6
UNIT=BOHR
ESTATE_LOCK=OFF
COORD=CARTESIAN
EOMFOLLOW=OVERLAP
SCF_DAMPING=500
SCF_EXPSTART=10
CHARGE=1
MEM=3
MEM_UNIT=GB)

CA:PCVTZ
N:PVTZ
H:PVTZ
H:PVTZ

%excite*
1
1
1  0  {ORB}  0  1.0


"""

# basis sets for CFOUR, in "GENBAS" file
GENBAStxt = """CA:PCVTZ
EMSL BASIS SET LIBRARY

  4
    0    1    2    3
    8    7    5    2
   22   16    8    2

 2402654.00000 359789.800000 81878.0900000 23190.8900000  7565.2120000
  2730.7020000  1064.6400000   441.0605000   191.7269000    86.5377400
    39.8992400    17.6406500     8.3599900     3.9513300     1.7134000
     0.8108600     0.3602500     0.0810800     0.0448400     0.0214300
     2.0630000     0.4098000

 0.0000093 -0.0000027  0.0000009 -0.0000002  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0000723 -0.0000210  0.0000072 -0.0000017  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0003805 -0.0001105  0.0000381 -0.0000091  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0016045 -0.0004666  0.0001610 -0.0000384  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0058078 -0.0016951  0.0005846 -0.0001396  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0185956 -0.0054834  0.0018950 -0.0004525  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0528777 -0.0159659  0.0055252 -0.0013203  0.0000000  0.0000000  0.0000000
 0.0000000
 0.1301514 -0.0415138  0.0144701 -0.0034584  0.0000000  0.0000000  0.0000000
 0.0000000
 0.2593147 -0.0928638  0.0327158 -0.0078368  0.0000000  0.0000000  0.0000000
 0.0000000
 0.3614961 -0.1653165  0.0600319 -0.0144151  0.0000000  0.0000000  0.0000000
 0.0000000
 0.2641116 -0.1766407  0.0670168 -0.0162164  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0570939  0.0644442 -0.0259366  0.0063442  0.0000000  0.0000000  0.0000000
 0.0000000
-0.0018220  0.5108796 -0.2674746  0.0674062  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0021116  0.4946380 -0.4269725  0.1144739  0.0000000  0.0000000  0.0000000
 0.0000000
-0.0009770  0.0875009  0.0679640 -0.0263447  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0004558 -0.0035910  0.7102053 -0.2336988  0.0000000  0.0000000  0.0000000
 0.0000000
-0.0001914  0.0024922  0.4418005 -0.3160753  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0000917 -0.0007582  0.0219313  0.3328193  1.0000000  0.0000000  0.0000000
 0.0000000
-0.0000787  0.0006458 -0.0118692  0.5611103  0.0000000  0.0000000  0.0000000
 0.0000000
 0.0000223 -0.0001817  0.0026527  0.2808178  0.0000000  1.0000000  0.0000000
 0.0000000
 0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  1.0000000
 0.0000000
 0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  0.0000000
 1.0000000

  4061.2890000   962.2465000   312.1686000   118.7144000    49.8067000
    22.2599800    10.2876400     4.8611540     2.2487730     1.0336620
     0.4641320     0.1987500     0.0673900     0.0254200     2.8806000
     0.5347000

 0.0001979 -0.0000645  0.0000133  0.0000000  0.0000000  0.0000000  0.0000000
 0.0017320 -0.0005645  0.0001185  0.0000000  0.0000000  0.0000000  0.0000000
 0.0095337 -0.0031312  0.0006487  0.0000000  0.0000000  0.0000000  0.0000000
 0.0383901 -0.0127408  0.0026799  0.0000000  0.0000000  0.0000000  0.0000000
 0.1167588 -0.0399140  0.0082851  0.0000000  0.0000000  0.0000000  0.0000000
 0.2562687 -0.0905044  0.0192123  0.0000000  0.0000000  0.0000000  0.0000000
 0.3797808 -0.1426189  0.0295498  0.0000000  0.0000000  0.0000000  0.0000000
 0.3082932 -0.1098090  0.0243123  0.0000000  0.0000000  0.0000000  0.0000000
 0.0859209  0.1516249 -0.0411123  0.0000000  0.0000000  0.0000000  0.0000000
 0.0021206  0.4617641 -0.1041975  0.0000000  0.0000000  0.0000000  0.0000000
 0.0012888  0.4326003 -0.1503653  0.0000000  0.0000000  0.0000000  0.0000000
-0.0004683  0.1112741  0.0243172  1.0000000  0.0000000  0.0000000  0.0000000
 0.0001472  0.0025287  0.5986116  0.0000000  0.0000000  0.0000000  0.0000000
-0.0000528  0.0007103  0.4813557  0.0000000  1.0000000  0.0000000  0.0000000
 0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  1.0000000  0.0000000
 0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  0.0000000  1.0000000

    16.9462300     4.4721200     1.4380900     0.4669900     0.1415100
     0.0416400     2.2775000     1.1270000

 0.0154730  0.0000000  0.0000000  0.0000000  0.0000000
 0.0788740  0.0000000  0.0000000  0.0000000  0.0000000
 0.2087800  0.0000000  0.0000000  0.0000000  0.0000000
 0.3302130  0.0000000  0.0000000  0.0000000  0.0000000
 0.4375620  1.0000000  0.0000000  0.0000000  0.0000000
 0.3747900  0.0000000  1.0000000  0.0000000  0.0000000
 0.0000000  0.0000000  0.0000000  1.0000000  0.0000000
 0.0000000  0.0000000  0.0000000  0.0000000  1.0000000

     0.1509000     1.3909000

 1.0000000  0.0000000
 0.0000000  1.0000000
 
N:PVTZ
JFS DUNNING CORRELATION CONSISTENT BASIS FROM FTP

  4
    0    1    2    3
    4    3    2    1
   10    5    2    1

 11420.0000000  1712.0000000   389.3000000   110.0000000    35.5700000
    12.5400000     4.6440000     1.2930000     0.5118000     0.1787000

 0.0005230 -0.0001150  0.0000000  0.0000000
 0.0040450 -0.0008950  0.0000000  0.0000000
 0.0207750 -0.0046240  0.0000000  0.0000000
 0.0807270 -0.0185280  0.0000000  0.0000000
 0.2330740 -0.0573390  0.0000000  0.0000000
 0.4335010 -0.1320760  0.0000000  0.0000000
 0.3474720 -0.1725100  0.0000000  0.0000000
 0.0412620  0.1518140  1.0000000  0.0000000
-0.0085080  0.5999440  0.0000000  0.0000000
 0.0023840  0.3874620  0.0000000  1.0000000

    26.6300000     5.9480000     1.7420000     0.5550000     0.1725000

 0.0146700  0.0000000  0.0000000
 0.0917640  0.0000000  0.0000000
 0.2986830  0.0000000  0.0000000
 0.4984870  1.0000000  0.0000000
 0.3370230  0.0000000  1.0000000

     1.6540000     0.4690000

 1.0000000  0.0000000
 0.0000000  1.0000000

     1.0930000

 1.0000000


H:PVTZ
JFS DUNNING CORRELATION CONSISTENT BASIS FROM FTP

  3
    0    1    2
    3    2    1
    5    2    1

    33.8700000     5.0950000     1.1590000     0.3258000     0.1027000

 0.0060680  0.0000000  0.0000000
 0.0453080  0.0000000  0.0000000
 0.2028220  0.0000000  0.0000000
 0.5039030  1.0000000  0.0000000
 0.3834210  0.0000000  1.0000000

     1.4070000     0.3880000

 1.0000000  0.0000000
 0.0000000  1.0000000

     1.0570000

 1.0000000
 """

# equilibrium Cartesian geometry in units of Bohr radii (COLUMBUS format, "geom")
geomtxt = """ Ca   20.0    0.00000000   -0.00000000   -1.19912624     0.00000000
 N     7.0    0.00000000   -0.00000000    2.84363110    14.00307401
 H     1.0   -1.51250280    0.00000000    4.01885944     1.00782504
 H     1.0    1.51250280    0.00000000    4.01885944     1.00782504"""

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
#SBATCH -N 1
#SBATCH -A dyarkon1
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
rm GENBAS script.sh ZMAT
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

def int_to_cart(intdisp = [0]*6, directory: str = "."):
    '''converts internal to Cartesian coordinates using COLUMBUS's cart2int.x
    intdisp: displacement in internal coordinates (defined by intcfl) from the reference geometry
        it is a list with 6 float elements, each corresponding to one of the 6 internal coordinates
        STRE (distance coordinates) are in Angstroms and all others (angular coordinates) are in radians
    directory: name of folder to work in for this geometry'''
    # copy required files into directory
    filewrite(geomtxt,    directory + "/geom")       # geom
    filewrite(cartgrdtxt, directory + "/cartgrd")    # dummy cartgrd
    filewrite(intcfltxt,  directory + "/intcfl")     # intcfl
    filewrite(i2ctxt,     directory + "/cart2intin") # cart2int input
    # write internal coordinate geometry to intgeomch
    min1 = np.array([2.13933521, 1.43344077, 1.82046465, 0.0, 0.0, 0.0]) # ground state minimum of CaNH2
    intgeom = min1 + np.array(intdisp) # add displacement
    partial_disp = np.zeros(len(intdisp))
    while True:
        # ensure coordinates are within 1 unit of equilibrium
        for coord in range(len(intdisp)):
            if abs(intdisp[coord] - partial_disp[coord]) > 0.5:
                #print("Abs(displacement in coordinate " + str(coord + 1) + ") > 0.5, so this is not the final geometry conversion step")
                partial_disp[coord] += 0.5*np.sign(intdisp[coord])
            else:
                partial_disp[coord] = intdisp[coord]
        g = open(directory + '/intgeomch', "w")
        firstline = True
        for coord in (min1 + partial_disp):
            if not firstline: # no need to write newline if it's the first line in the file
                g.write("\n")
            g.write(format(coord, "14.8f"))
            firstline = False
        g.close()
        # run cart2int to convert internal to Cartesian coordinates
        rv = subprocess.run([cart2int_loc + "/cart2int.x"], cwd="./" + directory, capture_output=True)
        if rv.stdout.decode('utf8'):
            print(rv.stdout.decode('utf8'))
        # replace geom with geom.new
        filecheck(directory + "/geom.new")
        os.system("mv " + directory + "/geom.new " + directory + "/geom")
        # check if another loop is not needed
        if (partial_disp == intdisp).all():
            break
    # ensure that the coordinate conversion was performed correctly
    filewrite(c2itxt, directory + "/cart2intin") # cart2int input
    rv = subprocess.run([cart2int_loc + "/cart2int.x"], cwd="./" + directory, capture_output=True)
    if rv.stdout.decode('utf8'):
        print(rv.stdout.decode('utf8'))
    int_geom_diff = np.array(getintcoord(directory)) - intgeom
    for coord in range(len(int_geom_diff)):
        if abs(int_geom_diff[coord]) > 0.000001:
            print("WARNING: Internal coordinate discrepancy of " + str(int_geom_diff[coord]) + " in coordinate " + str(coord + 1))
    # read geom
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
    atoms = ["CA", "N ", "H ", "H "]
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
        os.system("rm " + 
                  directory + "/bmatrix " + 
                  directory + "/bummer " + 
                  directory + "/cart2intin " +
                  directory + "/cart2intls " +
                  directory + "/cartgrd " +
                  directory + "/geom " +
                  directory + "/intcfl " +
                  directory + "/intgeomch")
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
    for i in [-0.16, -0.12, -0.08, -0.04, 0, 0.04, 0.08, 0.12, 0.16, 0.20]:
        for j in [-0.10, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.10]:
            for k in [-0.30, -0.24, -0.18, -0.12, -0.06, 0, 0.06, 0.12, 0.18, 0.24, 0.30, 0.33]:
                for l in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
                    for m in [-0.10, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.10]:
                        for n in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
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
#main()

# automatic
last_submitted = start - 1 # last job that was submitted
while last_submitted <= end:
    # check how many jobs are running
    rv = subprocess.check_output(['squeue -u $USER'], shell = True, text = True)
    batch_size = 400 - len(rv.split('\n')) # how many jobs to run this time
    main(last_submitted + 1, last_submitted + batch_size//3) # run the jobs
    last_submitted += batch_size//3
    time.sleep(120) # wait for the submitted jobs to run
