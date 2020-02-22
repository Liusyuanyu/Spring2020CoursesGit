def NewtonRaphson(fpoly, a, tolerance = .00001): 
    """Given a set of polynomial coefficients fpoly 
    for a univariate polynomial function, 
    e.g. (3, 6, 0, -24) for 3x^3 + 6x^2 +0x^1 -24x^0, 
    find the real roots of the polynomial (if any)  
    using the Newton-Raphson method. 
 
    a is the initial estimate of the root and  
    starting state of the search 
 
    This is an iterative method that stops when the 
    change in estimators is less than tolerance.    
""" 
    x0 = a
    fpoly_prime = derivative(fpoly)
    change = polyval(fpoly,x0)/polyval(fpoly_prime,x0) 
    while(abs(change) > tolerance):
        change = polyval(fpoly,x0)/polyval(fpoly_prime,x0) 
        x0 = x0 - change
    return x0


def polyval(fpoly, x): 
    """polyval(fpoly, x) 
    Given a set of polynomial coefficients from highest order to x^0, 
    compute the value of the polynomial at x.  We assume zero  
    coefficients are present in the coefficient list/tuple. 
 
    Example:  f(x) = 4x^3 + 0x^2 + 9x^1 + 3 evaluated at x=5 
    polyval([4, 0, 9, 3], 5)) 
    returns 548 
    """
    power = len(fpoly)-1
    value = 0
    for num in fpoly:
        value += num* x ** power
        power -=1
    return value 
 
def derivative(fpoly): 
    """derivative(fpoly) 
    Given a set of polynomial coefficients from highest order to x^0, 
    compute the derivative polynomial.  We assume zero coefficients 
    are present in the coefficient list/tuple. 
 
    Returns polynomial coefficients for the derivative polynomial. 
    Example: 
    derivative((3,4,5))  # 3 * x**2 + 4 * x**1 + 5 * x**0 
    returns:  [6, 4]     # 6 * x**1 + 4 * x**0 
    """ 
    power = len(fpoly)-1
    prime_fpoly = []
    fpoly = fpoly[:-1]
    for num in fpoly:
        prime_fpoly.append(num*power)
        power -=1
    return prime_fpoly
    