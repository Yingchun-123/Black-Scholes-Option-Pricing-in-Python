import math
from closed_form import closed_form_price
from mc_price import mc_price
from fdm_price import fdm_price
from option import Option, Call, Put
##from fem_price_log import fem_price_femlog

def main():
    S0=float(input("spot price: "))
    K=float(input("strike price: "))
    r=float(input("risk-free interest rate: "))
    sigma=float(input("volatility:"))
    T=float(input("Time to maturity:"))

    opt_call=Call(S0,K,r,sigma,T)
    opt_put=Put(S0,K,r,sigma,T)

    print("The Call Option")
    print (f"The price with closed_form is: {closed_form_price(opt_call, is_call=True)}")
    print (f"The price with Monte-Carlo Method is: {mc_price(opt_call, n=1000000,seed=50)}")
    print (f"The price with fed is:{fdm_price(opt_call,N=400,M=800)}")
    ##print (f"The price with Finit element Method is:{fem_price_femlog(opt_call,N=400,M=800)}")
    print("The Put Option")
    print (f"The price with closed_form is: {closed_form_price(opt_put,is_call=False)}")
    print (f"The price with Monte-Carlo Method is: {mc_price(opt_put, n=1000000,seed=50)}")
    print (f"The price with fed is:{fdm_price(opt_put,N=400,M=800)}")
main()
