#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import ceil, log
import time
import argparse

def read(filename1, filename2):
    lines1 = open(filename1, 'r').read().splitlines()
    lines1 = lines1[1:len(lines1)]

    lines2 = open(filename2, 'r').read().splitlines()
    lines2 = lines2[1:len(lines2)]

    A = []
    B = []
    matrix1 = A
    matrix2 = B
    for line in lines1:
        if line != "":
            matrix1.append(list(map(int, [x for x in  line.split("\t") if x])))
        else:
            matrix1 = C

    for line in lines2:
        if line != "":
            matrix2.append(list(map(int, [x for x in  line.split("\t") if x])))
        else:
            matrix2 = C

    return A, B


def add(A, B):
    n = len(A)
    C = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def subtract(A, B):
    n = len(A)
    C = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def strassen(A, B, seuil=1):
    """
        Implementation of the strassen algorithm.
    """
    n = len(A)
    newSize = n//2

    if n <= seuil:
        return conv(A, B)
    else:
        # initializing the new sub-matrices
       
        a11 = [[0 for j in range(newSize)] for i in range(newSize)]
        a12 = [[0 for j in range(newSize)] for i in range(newSize)]
        a21 = [[0 for j in range(newSize)] for i in range(newSize)]
        a22 = [[0 for j in range(newSize)] for i in range(newSize)]

        b11 = [[0 for j in range(newSize)] for i in range(newSize)]
        b12 = [[0 for j in range(newSize)] for i in range(newSize)]
        b21 = [[0 for j in range(newSize)] for i in range(newSize)]
        b22 = [[0 for j in range(newSize)] for i in range(newSize)]

        aResult = [[0 for j in range(newSize)] for i in range(newSize)]
        bResult = [[0 for j in range(newSize)] for i in range(newSize)]

        # dividing the matrices in 4 sub-matrices:
        for i in range(newSize):
            for j in range(newSize):
                a11[i][j] = A[i][j]            # top left
                a12[i][j] = A[i][j + newSize]    # top right
                a21[i][j] = A[i + newSize][j]    # bottom left
                a22[i][j] = A[i + newSize][j + newSize] # bottom right

                b11[i][j] = B[i][j]            # top left
                b12[i][j] = B[i][j + newSize]    # top right
                b21[i][j] = B[i + newSize][j]    # bottom left
                b22[i][j] = B[i + newSize][j + newSize] # bottom right

        # Calculating p1 to p7:
        aResult = add(a11, a22)
        bResult = add(b11, b22)
        p1 = strassen(aResult, bResult, seuil) # p1 = (a11+a22) * (b11+b22)

        aResult = add(a21, a22)      # a21 + a22
        p2 = strassen(aResult, b11,seuil)  # p2 = (a21+a22) * (b11)

        bResult = subtract(b12, b22) # b12 - b22
        p3 = strassen(a11, bResult, seuil)  # p3 = (a11) * (b12 - b22)

        bResult = subtract(b21, b11) # b21 - b11
        p4 =strassen(a22, bResult, seuil)   # p4 = (a22) * (b21 - b11)

        aResult = add(a11, a12)      # a11 + a12
        p5 = strassen(aResult, b22, seuil)  # p5 = (a11+a12) * (b22)

        aResult = subtract(a21, a11) # a21 - a11
        bResult = add(b11, b12)      # b11 + b12
        p6 = strassen(aResult, bResult, seuil) # p6 = (a21-a11) * (b11+b12)

        aResult = subtract(a12, a22) # a12 - a22
        bResult = add(b21, b22)      # b21 + b22
        p7 = strassen(aResult, bResult, seuil) # p7 = (a12-a22) * (b21+b22)

        # calculating c21, c21, c11 e c22:
        c12 = add(p3, p5) # c12 = p3 + p5
        c21 = add(p2, p4)  # c21 = p2 + p4

        aResult = add(p1, p4) # p1 + p4
        bResult = add(aResult, p7) # p1 + p4 + p7
        c11 = subtract(bResult, p5) # c11 = p1 + p4 - p5 + p7

        aResult = add(p1, p3) # p1 + p3
        bResult = add(aResult, p6) # p1 + p3 + p6
        c22 = subtract(bResult, p2) # c22 = p1 + p3 - p2 + p6

        # Grouping the results obtained in a single matrix:
        C = [[0 for j in range(n)] for i in range(n)]
        for i in range(newSize):
            for j in range(newSize):
                C[i][j] = c11[i][j]
                C[i][j + newSize] = c12[i][j]
                C[i + newSize][j] = c21[i][j]
                C[i + newSize][j + newSize] = c22[i][j]
        return C


def conv(A, B):
    n = len (A)
    C = [[0 for i in range(n)] for j in range(n)]
    for j in range(n):
        for i in range(n):
            for k in range(n):
                C[j][i] += A[k][i]*B[j][k]
    return C

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # parser.add_option("-l", dest="LEAF_SIZE", default="8",
    #      help="when do you start using ikj", metavar="LEAF_SIZE")

    parser.add_argument("algo")
    parser.add_argument("path1")
    parser.add_argument("path2")
    parser.add_argument("-p", "--print", action = "store_true")
    parser.add_argument("-t", "--time", action="store_true")

    args = parser.parse_args()
    A, B = read(args.path1, args.path2)

    start = 0
    end = 0
    seuil = 32
    if args.algo == 'strassen':
        start = time.time()
        C = strassen(A, B)
        end = time.time()
        
    elif args.algo == 'strassenSeuil':
        
        start = time.time()
        C = strassen(A, B, seuil)
        end = time.time()

    elif args.algo == 'conv':
        start = time.time()
        C = conv(A, B)
        end = time.time()
    else:
    	print ("argument de l'option -a invalides")
    
    if args.time: 
        resultat = end - start
        print(resultat)
