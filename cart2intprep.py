#this python file is used for when we are using our own internal coordinate system
#this converts our cartesian to internal using Columbus

orbs= ["24"]

import numpy as np
import os
import subprocess
import sys

pre = [" Sr   38.0", " N     7.0", " H     1.0", " H     1.0"]
post = ["    0.00000000\n", "   14.00307401\n", "    1.00782504\n", "    1.00782504\n"]

cartgrdtxt = """    0.739462D-07   0.107719D-01   0.359672D-02
  -0.637601D-07   0.573448D-03   0.113684D-01
  -0.408939D-07  -0.123975D-01  -0.519692D-02
   0.106949D-07  -0.150151D-02  -0.199053D-02"""

c2itxt = """ &input
    calctype='cart2int'
 /"""

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

def get_COL_dir() -> str:
    '''returns the directory of COLUMBUS'''
    return '/scratch16/lcheng24/zguo71/columbus/'

def filewrite(text: str, location: str):
    '''writes file to created directory
    text: text to write in the file
    location: path to the file to create'''
    f = open(location, "w")
    f.write(text)
    f.close()

cart2int_loc = get_COL_dir()

def filecheck(fl: str):
    '''checks for the presence of a file
    fl: path to the file to check
    quits the program with an error if the file is not present'''
    if not os.path.isfile(fl):
        sys.exit(fl + " is required, but is not present")

def getcartcoord(directory: str) -> list:
    '''this function go into ZMAT file to obtain
       the cartesian geometry and write it to a
       string of xyz coordinates
    '''
    filecheck(directory + "/24/ZMAT")
    with open(directory + "/24/ZMAT", "r") as f:
        lines = f.readlines()
    cartgeom = []
    for line in lines[1:5]:
        cart = line.split()
        for i, coord in enumerate(cart[1:]):
            cart[i+1] = float(coord)
        cartgeom.append(cart)
    return cartgeom

def geomwrite(cartgeom: list, directory: str):
    """this function writes the geomtry obtained from
       getcartcoord to columbus formate"""
    #atoms = ["SR", "N ", "H ", "H "]
    cartstr = ""
    print(cartgeom)
    for atom in range(len(cartgeom)):
        cartstr += pre[atom]
        #cartstr += atoms[atom]
        for coord in cartgeom[atom][1:]:
            cartstr += format(coord, "14.8f")
        cartstr += post[atom]
    print(cartstr)
    with open(directory + "/geom", "w") as f:
        f.write(cartstr)
        f.close()
#print(getcartcoord("0_0_0_0_0_0/24"))

dirs = [ f.name for f in os.scandir("./") if f.is_dir() ]
for directory in dirs:
    cart_c = getcartcoord(directory)
    geomwrite(cart_c, directory)
    filewrite(cartgrdtxt, directory + "/cartgrd")    # dummy cartgrd
    filewrite(intcfltxt,  directory + "/intcfl")     # intcfl
    filewrite(c2itxt,     directory + "/cart2intin") # cart2int input
    rv = subprocess.run([cart2int_loc + "/cart2int.x"], cwd="./" + directory, capture_output=True)
    if rv.stdout.decode('utf8'):
        print(rv.stdout.decode('utf8'))    
