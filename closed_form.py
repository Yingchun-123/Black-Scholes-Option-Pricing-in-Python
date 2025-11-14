import math
from option import Call, Put


def normal(x):
    n=0.5*(1+math.erf(x/math.sqrt(2.0)))
    return n
def closed_form_price(opt, is_call=True):
    S0 = opt.S0
    K  = opt.K
    r  = opt.r
    sigma = opt.sigma
    T  = opt.T
    d1 = (math.log(S0/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    if is_call:
        return S0*normal(d1) - K*math.exp(-r*T)*normal(d2)
    else:
        return K*math.exp(-r*T)*normal(-d2) - S0*normal(-d1)


##opt=Call(S0=100,K=100,r=0.05,sigma=0.2,T=1)
##print (call_price(opt))
