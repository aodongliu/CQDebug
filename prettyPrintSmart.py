import numpy as np
import sys

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
dim = int(sys.argv[2])

f = open(fname)
elements = []
mat = np.zeros((dim,dim))


line = next(f)
a = line[(line.find('{')+1):]
b = a[:((a.find('}')))]
elements = b.split(',')


for i in range(dim):
    for j in range(dim):
        #print('e index: ' + str(i*dim+j))
        #print('m index: ' + '(' +str(j) + ',' + str(i) + ')')
        mat[j,i] = float(elements[i*dim+j])

f.close()

outMatrix(mat)
