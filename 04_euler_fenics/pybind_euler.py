'''
This example integrates a 1st order ODE using euler's method 
using pure python implementation and a pybind11-cpp implementation
This is meant to compare the speedup of pybind11 for these type of tasks
'''

import numpy as np
import matplotlib.pyplot as plt
import sys
import time

# ------------------------------------------------------- #

import fenics as fe


def integrate(u0, f, t):
    nt = len(t)
    dt = t[1] - t[0]
    u = np.zeros( nt )
    u[0] = u0
    for i in range(1,len(t)):
        u[i] = u[i-1] + dt*f(t[i-1])
    return u

cpp_integrate = """
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
namespace py = pybind11;
#include <iostream>

double f( double t )
{
    return t;
}

/*
    Here I am passing the vector by reference using Eigen::Ref< > 
    which refer to the input numpy array
*/

Eigen::VectorXd
integrate( double u0, Eigen::Ref<Eigen::VectorXd> t )
{
    int nt = t.size();
    double dt = t[1] - t[0];
    Eigen::VectorXd u(nt);
    u[0] = u0;
    for (int i=1; i<nt; i++)
    {
        u[i] = u[i-1] + dt*f(t[i-1]);
    }
    return u;
}

PYBIND11_MODULE(SIGNATURE, m)
{
    m.def("integrate", &integrate);
}

"""

def f(t):
    return t

def main():
    '''
    du/dt = t
    u = t^2/2 + u0
    '''
    # Initialize a large problem
    nt = int(1e6)
    t = np.linspace(0, 1, nt, dtype=np.float64)
    u0 = 0
    u_exact = t**2/2 + u0

    # Compile inline cpp code using FEniCS module
    cpp_integrate_obj = fe.compile_cpp_code(cpp_integrate)

    # Time python integrate
    ts = time.time()
    u_num_py = integrate(u0, f, t)
    te_py = time.time()-ts

    # Time pybind11-cpp integrate
    ts = time.time()
    u_num_cpp = cpp_integrate_obj.integrate( u0, t )
    te_cpp = time.time()-ts

    # Report time
    print('Time py : %f seconds' % te_py)
    print('Time cpp: %f seconds' % te_cpp)
    print('Speedup: %f' % (te_py/te_cpp))


    # Check solution accuracy
    plt.plot( t[::(nt//20)], u_exact[::(nt//20)], 'r.', label='exact' )
    plt.plot( t, u_num_py, 'C0', label='pure python' )
    plt.plot( t, u_num_cpp, 'C1--', label='pybind11-cpp' )
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
