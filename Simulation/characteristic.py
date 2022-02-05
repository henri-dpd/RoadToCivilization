
from typing import List, Tuple
import math
import logging
import Simulation.operators as operators

class Characteristic:
    def __init__(self, name, value, limit_inf, limit_sup, mutability = 5, distr_function = None):
        self.name = name
        self.value = value
        self.limit_inf = limit_inf
        self.limit_sup = limit_sup
        self.mutability = mutability
        if distr_function == None:
            distr_function = operators.distribution_default
        self.distr_function = distr_function
        logging.info("Society has added/changed characteristic: %s with value:%s", name, value)
        
    def Change_Characteristic(self, name, value, lower = -math.inf, upper = math.inf, mutability = -1, distr_function = None):
        ret = True
        if lower > upper:
            lower = upper - 1
            ret = False
        if isinstance(value, List):
            if value[0] < lower:
                value[0] = lower
                ret = False
            if value[0] > upper:
                value[0] = upper
                ret = False
                
            if value[1] > upper:
                value[1] = upper
                ret = False
            if value[1] < lower:
                value[1] = lower
                ret = False
        else:
            if value < lower:
                value = lower
                ret = False
            if value > upper:
                value = upper
                ret = False
        
        if mutability == -1:
            mutability = self.mutability
        
        if distr_function == None:
            distr_function = self.distr_function
        
        self.name = name
        self.value = value 
        self.limit_inf = lower
        self.limit_sup = upper
        self.mutability = mutability
        self.distr_function = distr_function
        logging.info("Has added/changed characteristic: %s with value:%s", self.name, value)
        return ret
        
    def Update_Characteristic_Value(self, value):
        lower = self.limit_inf
        upper = self.limit_sup
        return self.Change_Characteristic(self.name, value, lower, upper)

    def Copy(self):
        return Characteristic(self.name, self.value, self.limit_inf, self.limit_sup, self.mutability, self.distr_function)
        