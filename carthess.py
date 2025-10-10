polynomial_degree = 6
import os
import sys
import numpy as np
import joblib
import subprocess
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#bohr2m = 0.529177249e-10
#hartree2joule = 4.35974434e-18
#speed_of_light = 299792458
#avogadro = 6.0221413e+23
#vib_constant = math.sqrt((avogadro*hartree2joule*1000)/(bohr2m*bohr2m))/(2*math.pi*speed_of_light*100)
freq2cm = 1378999.78 * 2 * np.pi
ht2cm = 219474.63137

#Read input_xabc
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

#Minimum and displacement
min1 = np.array([2.26268918, 1.43506504, 1.81432190, 0.0, 0.0, 0.0]) # ground state minimum of SrNH2 from cfour
#min2 is the actual surface minimum by subtracting the geom difference from opt.py
min2 = min1 - np.array([0.0019200113255312713, -0.0002240549094083047, 0.005224254081080706, -3.376642705258177e-14, 3.3387948329920475e-15, 1.8286039123597266e-14])
print(min2)
loaded_model = joblib.load('model4')

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

def filewrite(text: str, location: str):
    '''writes file to created directory
    text: text to write in the file
    location: path to the file to create'''
    f = open(location, "w")
    f.write(text)
    f.close()

def filecheck(fl: str):
    '''checks for the presence of a file
    fl: path to the file to check
    quits the program with an error if the file is not present'''
    if not os.path.isfile(fl):
        sys.exit(fl + " is required, but is not present")

def next_guess(rel_int:list, grad:list, n:float) -> list:
    rel_int = np.array(rel_int)
    grad = np.array(grad)
    next_geom = rel_int - n * grad
    return next_geom.tolist()

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

def geom_print(geometry):
    """write out geometry in Columbus format"""
    atom_data = [
            " Sr   38.0", "    0.00000000",
            " N     7.0", "   14.00307401",
            " H     1.0", "    1.00782504",
            " H     1.0", "    1.00782504"]
    out_str = ""
    for i in range(int(len(atom_data)/2)):
        out_str += atom_data[2*i]
        for j in range(3):
            out_str += format(float(geometry[3*i + j]), "14.8f")
        out_str += atom_data[2*i + 1] + "\n"
    return out_str

directory = '.'
def cart_to_int(cart):
    """converting cartesian to internal"""
    filewrite(c2itxt, directory + "/cart2intin") # cart2int input
    filewrite(geom_print(cart), directory + "/geom")       # geom
    filewrite(cartgrdtxt, directory + "/cartgrd")    # dummy cartgrd
    filewrite(intcfltxt,  directory + "/intcfl")     # intcfl
    rv = subprocess.run([cart2int_loc + "/cart2int.x"], cwd="./" + directory, capture_output=True)
    return getintcoord(directory) - min2
   

def getsurfE(cart):
    rel_int = cart_to_int(cart)
    rel_int = np.array(rel_int)
    relative_int = rel_int.reshape(1, -1)
    poly = PolynomialFeatures(polynomial_degree, include_bias = False)
    poly_features = poly.fit_transform(relative_int)
    output =  loaded_model.predict(poly_features)
    return output[0]

#https://www.chem.ualberta.ca/~massspec/atomic_mass_abund.pdf
m = np.array([87.905614, 14.003074, 1.007825, 1.007825])#amu 
amu2au = 1822.888486 #au/amu
m_au = m * amu2au #au
def mass_matrix():
    m3 = np.repeat(np.sqrt(m_au), 3)
    m3 = 1/m3
    return np.outer(m3, m3)

cur_geom = [0.00000000, 0.00000000, -0.68198419, 
        0.00000000, 0.00000000, 3.59387835, 
        -1.51059587, 0.00000000, 4.77508354,
        1.51059587, 0.00000000, 4.77508354]
h = 0.001

#Energy for minimum
E0 = getsurfE(cur_geom)
print(E0)
#Single coordinate displacements
dE = np.empty(12)
for i in range(len(cur_geom)):
    displaced = cur_geom.copy()
    displaced[i] += h
    dE[i] = getsurfE(displaced)
print("dE")
print(dE-E0)

#Pair-wise displacement
d2E = np.empty((12,12))
for i in range(len(cur_geom)):
    for j in range(i, len(cur_geom)):
        displaced = cur_geom.copy()
        displaced[i] += h
        displaced[j] += h
        d2E[i,j] = getsurfE(displaced)
print("d2E")
print(d2E-E0)
#finite difference hessian
HESS = np.empty((12,12))
for i in range(len(cur_geom)):
    for j in range(i, len(cur_geom)):
        HESS[i,j] = (d2E[i,j] - dE[i] - dE[j] + E0) / h**2
        if i != j: 
            HESS[j,i] = HESS[i,j]
print("HESS")
print(HESS)
mass_hess = mass_matrix() * HESS
eigenvalues, eigenvectors = np.linalg.eigh(mass_hess)
print("eigenvalues")
print(eigenvalues)
np.set_printoptions(precision=3, suppress=True, linewidth=np.inf)

freq_cm = np.sqrt(eigenvalues) * ht2cm
print("freq")
print(freq_cm)

