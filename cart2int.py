import numpy as np
import sys
import os

bh2ag = 0.529177
DEG2RAD = np.pi / 180.0

def getcartcoord(directory: str) -> list:
    '''this function go into ZMAT file to obtain
       the cartesian geometry and write it to a
       string of xyz coordinates
    '''
    with open(directory + "/24/ZMAT", "r") as f:
        lines = f.readlines()
    cartgeom = []
    for line in lines[1:5]:
        cart = line.split()[1:]
        for i, coord in enumerate(cart):
            cart[i] = float(coord)
        cartgeom.append(cart)
    return cartgeom

def angle_deg(a, b, c):
        v1 = a - b 
        v2 = c - b
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)
        cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        if cosang > 1.0:
            cosang = 1.0
        elif cosang < -1.0: 
            cosang = -1.0
        return np.arccos(cosang) * 180.0 / np.pi

def angle_SrN_to_NHH_plane_rad(cart):

    Sr = np.array(cart[0])
    N = np.array(cart[1])
    H1 = np.array(cart[2])
    H2 = np.array(cart[3])
    v = Sr - N
    n = np.cross((H1 - N), (H2 - N))
    v_norm = v / np.linalg.norm(v)
    n_norm = n / np.linalg.norm(n)
    if (np.linalg.norm(v) < 1e-15) or (np.linalg.norm(n) < 1e-15):
        print("if ran")
        return 0.0
    s = np.dot(v_norm, n_norm)
    print(s)
    if s > 1:
        s = 1
    if s < -1:
        s = -1
    return np.arcsin(s)

def cart2int(cart):
    
    r0 = np.array(cart[0])
    r1 = np.array(cart[1])
    r2 = np.array(cart[2])
    r3 = np.array(cart[3])

    zhat = np.array([0.0, 0.0, 1.0])

    v_SrN = r1 - r0    #Sr-N bond vector
    v_SrN_normal = v_SrN / np.linalg.norm(v_SrN)

    R01   = np.linalg.norm(r0 - r1) #Sr-N bondlength
    R12   = np.linalg.norm(r1 - r2) #N-H1 bondlength
    R13   = np.linalg.norm(r1 - r3) #N-H2 bondlength

    A012  = angle_deg(r0, r1, r2)   #SrNH1 angle
    A013  = angle_deg(r0, r1, r3)   #SrNH2 angle
    A231  = angle_deg(r2, r1, r3)   #HNH angle

    internal = np.zeros(6)
    SQRT2 = np.sqrt(2.0);
    internal[0] = R01 * bh2ag                                   #IC1: SrN stretching
    internal[1] = ((R12 + R13) / SQRT2) * bh2ag                 #IC2: Symmetric stretching of NH bonds
    internal[2] = A231 * DEG2RAD                                #HNH angle in radians
    internal[3] = angle_SrN_to_NHH_plane_rad(cart)              #IC4: SrN to NHH plane angle
    internal[4] = ((R12 - R13) / SQRT2) * bh2ag                 #IC5: Assymmetric stretching of NH bonds
    internal[5] = ((A013 - A012) / SQRT2) * DEG2RAD             #IC6: SrNH1 - SrNH2 angle
    return internal

cart = getcartcoord("./")
print(cart2int(cart))
