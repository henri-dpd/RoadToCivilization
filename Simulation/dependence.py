
from typing import List, Tuple
import math
import logging

#from numpy import true_divide
import Simulation.operators as operators

class Dependence:
    def __init__(self, pos_1, entity_1, characteristic_1,
                       pos_2, entity_2, characteristic_2,
                       c, plus_function = None, mult_function = None):
        self.pos_1 = pos_1
        self.entity_1 = entity_1
        self.characteristic_1 = characteristic_1
        self.pos_2 = pos_2
        self.entity_2 = entity_2
        self.characteristic_2 = characteristic_2
        self.c = c
        if plus_function == None:
            plus_function = operators.default_sum
        self.plus_function = plus_function
        if mult_function == None:
            mult_function = operators.default_mul
        self.mult_function = mult_function
        logging.info("dependence was added")
        
    def IsInstance(self, other):
        if (self.pos_1 == other.pos_1 and self.entity_1 == other.entity_1 and
           self.characteristic_1 == other.characteristic_1 and
           self.pos_2 == other.pos_2 and self.entity_2 == other.entity_2 and
           self.characteristic_2 == other.characteristic_2):
            return True
        return False

    def Change_C(self, c):
        self.c = c
        
    def Get_A(self):
        return (self.pos_1, self.entity_1, self.characteristic_1)
    
    def Get_B(self):
        return (self.pos_2, self.entity_2, self.characteristic_2)
    
    def Is_In(self, ab):
        return ab == self.Get_A or ab == self.Get_B

    def Copy(self):
        return Dependence(self.pos_1, self.entity_1, self.characteristic_1,
                          self.pos_2, self.entity_2, self.characteristic_2,
                          self.c, self.plus_function, self.mult_function)