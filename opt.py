polynomial_degree = 6
import numpy as np
import joblib
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
#Read input_xabc

#Minimum and displacement
min1 = np.array([2.26268918, 1.43506504, 1.81432190, 0.0, 0.0, 0.0]) # ground state minimum of SrNH2
loaded_model = joblib.load('model')

def getsurfE(rel_int):
    rel_int = np.array(rel_int)
    relative_int = rel_int.reshape(1, -1)
    poly = PolynomialFeatures(polynomial_degree, include_bias = False)
    poly_features = poly.fit_transform(relative_int)
    output =  loaded_model.predict(poly_features)
    return output[0]

def getgrad(rel_int:list, disp:float) -> list: 
    """This will evaluate the gradient with finite differences
    rel_int is the relative internal coordinates
    disp is the finite difference displacement"""  
    grad = []
    print(getsurfE(rel_int))
    for i in range(len(rel_int)):
        #positive displacement
        displaced = rel_int.copy()
        displaced[i] += disp
        E1 = getsurfE(displaced)
        #negative displacement
        displaced = rel_int.copy()
        displaced[i] -= disp
        E2 = getsurfE(displaced)
        #finite difference calculation
        grad.append((E1 - E2)/(2*disp))
    print("Gradient:", grad)
    return grad

def next_guess(rel_int:list, grad:list, n:float) -> list:
    rel_int = np.array(rel_int)
    grad = np.array(grad)
    next_geom = rel_int - n * grad
    return next_geom.tolist()

cur_geom = [0, 0, 0, 0, 0, 0]
threshold_reached = False 
n = 0.1
iteration = 0
while not threshold_reached:
    iteration += 1
    print(iteration)
    disp = 0.001   # finite difference step
    grad = getgrad(cur_geom, disp)
    cur_geom = next_guess(cur_geom, grad, n)
    if np.linalg.norm(grad) < 0.0001:
        threshold_reached = True
print(cur_geom)
print(grad)
print("Minimum has been reached")
