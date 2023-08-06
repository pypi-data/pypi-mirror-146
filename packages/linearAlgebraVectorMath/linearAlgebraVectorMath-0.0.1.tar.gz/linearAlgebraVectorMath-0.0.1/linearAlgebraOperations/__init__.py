import basicOperations 
import globalFunctions as gf
import matrixOperations as mo

def mult(a, b):
    if all(isinstance(x, list) for x in a) and all(isinstance(x, list) for x in b):
        return basicOperations.matrixMultiply(a,b)
    else:
        gf.errorTraceback()
        gf.printError('List of lists not found for matrices A and B')

# Working multiplication
#print(mult([[1,2]], [[3,4], [5,6]]))
# Intential Error:
#print(mult([1,2], [[3,4]]))

def add(a, b):
    if all(isinstance(x, list) for x in a) and all(isinstance(x, list) for x in b):
        return basicOperations.matrixAdd(a,b)
    else:
        gf.errorTraceback()
        gf.printError('List of lists not found for matrices A and B')

def sub(a, b):
    if all(isinstance(x, list) for x in a) and all(isinstance(x, list) for x in b):
        return basicOperations.matrixSub(a,b)
    else:
        gf.errorTraceback()
        gf.printError('List of lists not found for matrices A and B')

# Working addition
#print(add([[1,2], [7,8]], [[3,4], [5,6]]))
# Intential Error:
#print(sub([[1,2] , [1,1]], [[3,4] , [5,6]]))

def determinent(a):
    if all(isinstance(x, list) for x in a):
        return mo.determinent(a)
    else:
        gf.errorTraceback()
        gf.printError('List of lists not found for the matrix')

# Working 
#print(determinent([[1,2] , [3,4]]))
# Failure
#print(determinent([[1,2]]))

def transpose(a):
    if all(isinstance(x, list) for x in a):
        return mo.transposeMatrix(a)
    else:
        gf.errorTraceback()
        gf.printError('List of lists not found for the matrix')

# Working 
# print(transpose([[1,2,6,7] , [3,4,5,5], [5,6,3,2]]))

def inverse(a):
    if all(isinstance(x, list) for x in a):
        return mo.inverseMatrix(a)
    else:
        gf.errorTraceback()
        gf.printError('List of lists not found for the matrix') 

# Working 
#print(inverse([[1,2,3] , [3,4,6], [3,4,5]]))

