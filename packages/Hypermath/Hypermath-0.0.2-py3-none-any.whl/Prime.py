import gmpy2
import random 
def Pi(n):
    gmpy2.get_context().precision = n
    S = gmpy2.mpfr(426880)
    M = gmpy2.mpfr(gmpy2.sqrt(10005))
    G = gmpy2.mpfr(13591409)
    return (S*M)/G
def E(n):
    return gmpy2.exp(1)
def Lucas_Lehmer_Test(n):
    S =gmpy2.mpz(4)
    M_p = (gmpy2.mpz(2)**gmpy2.mpz(n))-1
    print(M_p)
    if gmpy2.is_prime(n):
        for _ in range(1, n-1):
            S = ((S**2)-2)%M_p
        return S==0
    else:
        return False
def Miller_Rabin_Test(n):
    if n < 2 or not n & 1:
        return False
    if n == 2:
        return True
    t = gmpy2.mpz(n - 1)
    def mrtest(b):
        x = gmpy2.powmod(b, t, n)
        if x == 1:
            return True
        for i in range(s):
            if x == n - 1:
                return True
            x = gmpy2.powmod(x, 2, n)
        return False
    s = gmpy2.mpz(0)
    while not t & 1:
        s += 1
        t >>= 1
    for i in range(10000):
        b = random.randrange(2, n)
        if not mrtest(b):
            return False
    return True
def Factorization(n):
    Factor = gmpy2.mpz(2)
    Factors = []
    while Factor**2 <= n:
        while n%Factor == 0:
            Factors.append(int(Factor))
            n = n//Factor
            Factor = Factor+1
        if n>1: 
            Factors.append(int(n))
    return Factors
def Euler_Phi(n):
    phi = int(n > 0 and n)
    m = gmpy2.mpz(n)**0.5
    m = int(m)+1
    for p in range(2, m):
        if not n%p:
            phi -= phi // p
            while not n%p: n //= p
    if n > 1: phi -= phi // n
    return phi
def Eratosthenes_Sieve(n):
    m = gmpy2.mpz(n**0.5)+1
    Primes = [True]*(n+1)
    for I in range(2, m):
        if Primes[I] == True:
            for J in range(I+I, n+1, I):
                Primes[J] = False
    Primes = [I for I in range(2, n+1) if Primes[I] == True]
    return Primes
def GCD(*Integers):
    return gmpy2.gcd(*integers)
def LCM(*Integers):
    return gmpy2.lcm(*integers)
def LLLTest(k):
    from functools import reduce
    import math
    n = Factorization(k+1)
    d = n.count(2)
    while 2 in n:
        n.remove(2)
    m = n[0]
    n = d
    if n > (2**m):
        return -1
    if m%4==1:
        return LLTest(k)
    elif m%4==3 or n%4==1:
        s = 5778
    elif k%6 == 5 or k%6==1:
        s = math.ceil((2+(3**0.5))**m)
    else:
        import sympy
        P = sympy.Symbol('P')
        Solve = sympy.solvers.solve((P-2)/n, P)
        s = Solve
    for _ in range(d-1):
        s = ((s**2)-2)%k
    return s==0
