from option import Option, Call, Put
import math, random
def mc_price(opt:Option, n=1000000,seed=50):
    if seed is not None:
        random.seed(seed)

    S0=opt.S0
    K=opt.K
    r=opt.r
    sigma=opt.sigma
    T=opt.T

    s=0
    for _ in range(n):
        Z=random.gauss(0,1)
        ST=S0*math.exp((r-0.5*sigma*sigma)*T+sigma*math.sqrt(T)*Z)
        s+=opt.payoff(ST)
        price=math.exp(-r*T)*(s/n)
    return price


##opt=Call(S0=100,K=100,r=0.05,sigma=0.2,T=1)
##print (mc_price(opt, n=1000000,seed=50))
