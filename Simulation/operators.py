import random as r
import math
from typing import List

def default_sum(a,b):
    if isinstance(a, List) and len(a) == 1:
        a = a[0]
    if isinstance(b, List) and len(b) == 1:
        b = b[0]
    if isinstance(a,List):
            if isinstance(b,List):
                return [a[0] + b[0], a[1] + b[1]]
            return [a[0] + b, a[1] + b]
    return a + distribution_default(b)

def default_mul(a,b):
    if isinstance(a, List) and len(a) == 1:
        a = a[0]
    if isinstance(b, List) and len(b) == 1:
        b = b[0]
    if isinstance(b,List):
            return [b[0] * a, b[1] * a]
    return a * b

def dependence(plus = default_sum, mul =default_mul):
    
    def func(a, b, c):
        if isinstance(a, List) and len(a) == 1:
            a = a[0]
        if isinstance(b, List) and len(b) == 1:
            b = b[0]
        if isinstance(c, List) and len(c) == 1:
            c = c[0]
            
        mul_result = mul(a,c)
        if isinstance(mul_result, List) and len(mul_result) == 1:
            mul_result = mul_result[0]
            
        plus_result = plus(b,mul_result)
        if isinstance(plus_result, List) and len(plus_result) == 1:
            plus_result = plus_result[0]
            
        return plus_result
        
    return func   
    

def influence(plus = default_sum, mul =default_mul):
    def func(old_a, act_a, b, c):
        if isinstance(old_a, List) and len(old_a) == 1:
            old_a = old_a[0]
        if isinstance(act_a, List) and len(act_a) == 1:
            act_a = act_a[0]
        if isinstance(b, List) and len(b) == 1:
            b = b[0]
        if isinstance(c, List) and len(c) == 1:
            c = c[0]
        negative = mul(old_a, -1) 
        negative = negative[0] if isinstance(negative, List) and len(negative) == 1 else negative
        diff = plus(act_a, negative) 
        diff = diff[0] if isinstance(diff, List) and len(diff) == 1 else diff
        mult = mul(diff, c)
        mult = mult[0] if isinstance(mult, List) and len(mult) == 1 else mult
        summ = plus(b, mult)
        return summ[0] if isinstance(summ, List) and len(summ) == 1 else summ        
    return func
    


def distribution_default(c):
    return r.randint(round(c[0]), round(c[1])) if isinstance(c, List)and len(c) ==2 else c

#continuas

def uniform(values):
    if len(values) != 2:
        raise Exception("Uniform Distribution needs two values")
    a = values[0]
    b = values[1]
    U = r.random()
    return (b-a)*U + a



def exponential(_lambda):
    if len(_lambda) != 1:
        raise Exception("Exponential Distribution needs only one values")
    _lambda = _lambda[0]
    U = r.random()
    return -(1/_lambda)*math.log(U)



def gamma(values):
    if len(values) != 2:
        raise Exception("Gamma Distribution needs two values")
    n = values[0]
    _lambda = values[1]
    Un = math.prod([r.random() for _ in range(int(n))])
    return -(1/_lambda)*math.log(Un)




def normal(values):
    if len(values) != 2:
        raise Exception("Normal Distribution needs two values")
    mu = values[0]
    o_2 = values[1]
    exp = exponential([1])
    while True:
        Y = exp
        U = r.random()
        if U <= math.exp((-1/2)*(Y-1)**2):
            break

    U = r.random()
    Z = Y if U < 0.5 else -Y

    # Z = (X - miu)/o ~ N(0,1) => X = Zo + miu ~ N(miu,o^2)
    return Z*math.sqrt(o_2) + mu


# discretas

def binomial(values):
    if len(values) != 2:
        raise Exception("Binomial Distribution needs two values")
    n = values[0]
    p = values[1]
    X = 0
    for _ in range(int(n)):
        U = r.random()
        if U <= p:
            X += 1
        else:
            X += 0
    return X


def geometric(p):
    if len(p) != 1:
        raise Exception("Geometric Distribution needs only one values")
    p = p[0]
    U = r.random()
    return math.ceil(math.log(U) / math.log(1-p))


