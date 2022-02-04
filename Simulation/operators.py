import random as r
import math
from typing import List

def default_sum(a,b):
    if isinstance(a,List):
            if isinstance(b,List):
                return [a[0] + b[0], a[1] + b[1]]
            return [a[0] + b, a[1] + b]
    return a + distribution_default(b)

def default_mul(a,b):
    if isinstance(b,List):
            return [b[0] * a, b[1] * a]
    return a * b

def dependence(plus = default_sum, mul =default_mul):
    return lambda a, b, c : plus(b, mul(a, c))

def influence(plus = default_sum, mul =default_mul):
    return lambda old_a, act_a, b, c : plus(b, mul(plus(act_a, mul(old_a, -1)), c))


def distribution_default(c):
    return r.randint(round(c[0]), round(c[1])) if isinstance(c, List) else c

#continuas

def uniform( a, b):
    U = r.random()
    return (b-a)*U + a



def exponential(_lambda):
    U = r.random()
    return -(1/_lambda)*math.log(U)



def gamma(n, _lambda):
    Un = math.prod([r.random() for _ in range(int(n))])
    return -(1/_lambda)*math.log(Un)




def normal( mu, o_2):
    exp = exponential(1)
    while True:
        Y = exp.get()
        U = r.random()
        if U <= math.exp((-1/2)*(Y-1)**2):
            break

    U = r.random()
    Z = Y if U < 0.5 else -Y

    # Z = (X - miu)/o ~ N(0,1) => X = Zo + miu ~ N(miu,o^2)
    return Z*math.sqrt(o_2) + mu


# discretas

def binomial(n, p):
    X = 0
    for _ in range(int(n)):
        U = r.random()
        if U <= p:
            X += 1
        else:
            X += 0
    return X


def geometric(p):
    U = r.random()
    return math.ceil(math.log(U) / math.log(1-p))


