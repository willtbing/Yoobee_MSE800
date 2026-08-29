import numpy as np

class matrix:
    def __init__(self):
        pass

    def input_matrix(self, rows, cols):
        mtx = []
        for i in range(rows):
            row = list(map(int, input().split()))
            mtx.append(row)
        A = np.array(mtx)
        return A

    def mul_matrix(self, A, B):
        return A @ B

print("Please input the first matrix's rows:")
rows = int(input())
print("Please input the first matrix's cols:")
cols = int(input())
print("Please input the items in the first matrix:")
max1 = matrix()
A = max1.input_matrix(rows, cols)

print("Please input the second matrix's rows:")
rows = int(input())
print("Please input the second matrix's cols:")
cols = int(input())
print("Please input the items in the second matrix:")
max2 = matrix()
B = max2.input_matrix(rows, cols)

print("The result of their multiplication is:")
C = max1.mul_matrix(A, B)
print(C)
    
