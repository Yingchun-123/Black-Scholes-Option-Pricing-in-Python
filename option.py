class Option:
    def __init__(self,S0,K,r,sigma,T):
        if S0<=0.0 or K<=0 or sigma<=0 or T<=0:
            raise ValueError("S0,K,sigma,T must be >0!!!")
        self.S0=S0
        self.K=K
        self.r=r
        self.sigma=sigma
        self.T=T

     ##def payoff(self,ST):


class Call(Option):
    def payoff(self,ST):
        if ST-self.K >0:
            return ST-self.K
        else:
            return 0

class Put(Option):
    def payoff(self,ST):
        if self.K-ST>0:
            return self.K-ST
        else:
            return 0


