from __future__ import division
import numpy as np
import scipy.linalg as slg
import math
import sys
from numpy import genfromtxt
import csv
from numpy import linalg as LA
from numpy.linalg import inv
import sys

def str2float(s):
    return float(s.replace('D','e'))

def CutLTMatOut(fname, head_line, index=0):
    cur_index = 0
    f = open(fname)
    status = None
    r = 0
    indices = []
    mat = []
    for line in f:
        if head_line in line:
            status = "Column Indices"
            continue
        if status == "Rows":
            splitted = line.split()
            if all([x.isnumeric() for x in splitted]):
                status = "Column Indices"
            else:
                try:
                    r = int(splitted[0])
                    floats = [str2float(s) for s in splitted[1:]]
                    if len(mat) < r:
                        mat.append(floats)
                    else:
                        mat[r-1] += floats
                except ValueError as e:
                    break
                continue
        if status == "Column Indices":
            status = "Rows"
            indices = [int(I) for I in line.split()]
            continue
    f.close()
    return mat

def toNPMatrix(mat_array, symmetry = 'symmetric'):
    dim = len(mat_array)
    mat = np.zeros((dim,dim))
    for i in range(dim):
        mat[i,:i+1] = mat_array[i]
    if symmetry == 'symmetric':
        diag = np.diag(np.diag(mat))
        return mat + mat.T - diag
    elif symmetry == 'anti-symmetric':
        return mat - mat.T


def ReadMatrix(fname, head_line, index=0):
    return np.array(CutLTMatOut(fname, head_line, index))

def ReadLowerTri(fname, head_line, index=0, symmetry = 'symmetric'):
    return toNPMatrix(CutLTMatOut(fname, head_line, index), symmetry)

def outMatrix(A):
    if np.iscomplexobj(A):
        print("Real part:")
        outMatrix(A.real)
        print()
        print("Imag part:")
        outMatrix(A.imag)
        return
    print("--------------------------------------------------------------------------------")
    curColStart, curColEnd = 0, 5
    while curColStart < A.shape[1]:
        curColEnd = min(curColStart + 5, A.shape[1])
        print("     "+"               ".join(list(map(str, range(curColStart + 1, curColEnd + 1)))))
        for i in range(A.shape[0]):
            print("%3d   "%(i+1,) + " ".join(list(map(lambda x : "%15.8e"%(x if abs(x) > 1e-8 else 0,) , A[i, curColStart : curColEnd]))))
        curColStart += 5
        print()

    print("--------------------------------------------------------------------------------")

fname =  sys.argv[1]
fheadline = sys.argv[2]
print(fname)
print(fheadline)
mat = ReadMatrix(fname, fheadline)

dim = len(mat)
for i in range(dim):
    for j in range(dim):
        if(j <= i):
            print("{:.12f}".format(mat[i,j]))

outMatrix(mat)


