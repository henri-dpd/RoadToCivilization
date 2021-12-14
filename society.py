import random
from typing import List, Tuple
import logging
import math


class Society:

    def __init__(self, name,specie):

        self.name = name
        self.specie = specie

        self.characteristic = {}
        self.characteristic_dependences = [] # dependence_1 -> dependence_2 * value
        self.characteristic_influences = [] # influence_1 -> influence_2 * value
        #self.characteristic_limits = [] # limit_1 -> limit_2 * value
        self.operators = {
            "dependence": (lambda a, b, c : self.sum(b, self.mul(a, c))),
            "influence": (lambda old_a, act_a, b, c : self.sum(b, self.mul(self.sum(act_a, self.mul(old_a, -1)), c))),
            #"limit": (lambda a, b, c : b if b < self.mul(a, c) else self.mul(a, c)),
            }
        self.distributions = {
            "default": lambda c: random.randint(round(c[0]), round(c[1])) if isinstance(c, List) else c
        }
        
        logging.info("Society was created")

    #Toma el valor de la caracteristica de entrada
    def Get_Characteristic_Value(self, name):
        return self.characteristic[name][0]

    # Con este método podemos añadir o modificar el valor de una caracteristica
    #lower limite inferior, upper  limite superior
    def Change_Characteristic(self, name, value, lower = -math.inf, upper = math.inf):
        if lower > upper:
            lower = upper - 1
        if isinstance(value, List):
            if value[0] < lower:
                value[0] = lower
            if value[0] > upper:
                value[0] = upper
                
            if value[1] > upper:
                value[1] = upper
            if value[1] < lower:
                value[1] = lower
        else:
            if value < lower:
                value = lower
            if value > upper:
                value = upper
        self.characteristic[name] = (value, lower, upper)
        logging.info("Society has added/changed characteristic: %s with value:%s", name, value)

    # Con este método podemos eliminar una característica
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("Society has deleted characteristic: %s", name)
            for i, dependence in enumerate(self.characteristic_dependences):
                if name in dependence:
                    del(dependence[i])
            return
        logging.warning("Society has not deleted characteristic: %s", name)

    #Actualiza el valor de una caracteristica existente, tomando el mismo lower y upper
    def Update_Characteristic_Value(self, name, value):
        lower = self.characteristic[name][1]
        upper = self.characteristic[name][2]
        self.Change_Characteristic(name, value, lower, upper) 
    
    #Pone caracteristicas por defecto
    def Set_Default_Characteristics(self):        
        self.Change_Characteristic("population", 1, 0)              #Poblacion
        self.Change_Characteristic("death_rate", [0, 1], 0)         #Mortalidad
        self.Change_Characteristic("birth_rate", [0, 1], 0)         #Natalidad
        self.Change_Characteristic("life_expectation", 1, 0)        #Esperanza de vida
        self.Change_Characteristic("gestation", 1, 0)               #Período de Gestación
        self.Change_Characteristic("reproduction_number", [0,1], 0) #Número de reproducción
        self.Change_Characteristic("size", 1, 0)                    #Tamaño
        self.Change_Characteristic("intellect", 1, 0)               #Intelecto
        self.Change_Characteristic("strength", 1, 0)                #Fuerza
        self.Change_Characteristic("evolution_rate", 1)          #Capacidad de evolución
        self.Change_Characteristic("actual_growth", 1)           #Crecimiento Actual
        self.Change_Characteristic("economy", 1)                 #Economía
        self.Change_Characteristic("foreign_tolerance", 1)       #Tolerancia a extranjeros
        logging.info("Society has added default characteristic")
