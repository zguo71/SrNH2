geomkick.py: creates new geometries using optimized ground state energy. create ZMAT file and submit it. 
runpolyreg.py: grep all the energies in the slurm file and then create the input file for surface fitting
surface-fit.py: do the surface fitting with scikit learn in python. 
exclude.py: search for all the results and rewrite an input file using the points that has a relative energy less than 2000k
error.py: look at the distribution of points and then list out the points with highest and lowest error. 
