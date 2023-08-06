import pyecm
import math
from math import sqrt
from gmpy2 import is_bpsw_prp as Is_Prime
import primefac
from iteration_utilities import deepflatten as Flatten
import gmpy2
from Crypto.Util.number import *
def ECM_Factorize(n):
    x = list(pyecm.factors(n, False, False, 2*math.log(math.log(n)), 1.0))
    for Idx in range(len(x)):
        x[Idx] = int(x[Idx])
    return x
def Primefac_Factorize(n):
    return list(primefac.primefac(n))
def Fermat_Factorise(n):
    assert n % 2 != 0, 'Not a Odd Number'
    if int(n) != n: raise Exception('N is not be a Float')
    if n != abs(n): raise Exception('N is Greater Than 0')
    if n == 0: raise Exception('N is not a 0')
    a = gmpy2.isqrt(n)
    b2 = gmpy2.square(a) - n
    for i in range(100000000):
        a += 1
        b2 = gmpy2.square(a) - n

        if gmpy2.is_square(b2):
            p = a + gmpy2.isqrt(b2)
            q = a - gmpy2.isqrt(b2)
            return int(p), int(q)
def Factorize(N):
    def Factorise(N):
        mL = int(sqrt(N)); mR = mL
        temp1 = mL*mR
        if temp1 == N: r = 0
        mR = int(N/mL)
        r = int(N%mL)
        while r != 0:
            mL -= 1
            r = int(mR + r)
            temp1 = int(r/mL)
            mR += temp1
            r = r%mL
        if Is_Prime(mL) == False:
            mL = Factorize(mL)
        if Is_Prime(mR) == False:
            mR= Factorize(mR)
        return [mL, mR]
    Factors = list(Flatten(Factorise(N)))
    return Factors
