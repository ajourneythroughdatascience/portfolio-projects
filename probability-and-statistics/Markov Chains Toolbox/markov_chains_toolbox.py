# Author: Pablo Aguirre
# This script includes a collection of functions design to aid in typical Markov Chain associated calculations.

import numpy as np
import scipy as sc


def simRandomWalk(A):
    pass

def steadyState(A):
    '''

    Parameters
    ----------
    A : Two-Dimensional Array
        Numpy array denoting transition matrix for a given Markov system.

    Returns
    -------
    pi_normalized : One-Dimensional Array
        NumPy array denoting steady-state probabilities for each state.

    '''
    
    # Compute left eigenvectors
    values, left = sc.linalg.eig(A, right = False, left = True)
    
    # Compute pi
    pi = left[:,0]
    print(pi)
    # Normalize eigenvector values (divide by sum)
    pi_normalized = np.array([(x/np.sum(pi)).real for x in pi])

    
    return pi_normalized

a11 = 0.4
a12 = 0.6
a13 = 0.0
a21 = 0.4
a22 = 0.2
a23 = 0.4
a31 = 0.0
a32 = 0.0
a33 = 1.0

A = np.array([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])
b = steadyState(A)