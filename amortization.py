#!/usr/bin/python3

import sys
import math

def i_amortize(p,r,n):
    # calculate the monthly interest rate
    # and produce a payment amount for to return
    r = r/12
    a = p*( (r*((1+r)**n))/((1+r)**n-1) )
    return(a)

def zero_interest(p,n):
    # calculate the monthly payment for a
    # zero interest loan
    a = p/n
    return(a)

if __name__ == "__main__":
    pri = int(sys.argv[1])
    rte = float(sys.argv[2])
    trm = int(sys.argv[3])

    if rte == 0:
        o_put = zero_interest(pri,trm)
    else:
        pct = rte*.01
        o_put = i_amortize(pri,pct,trm)
    
    print(round(o_put,2))
