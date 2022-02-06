
from Simulation.characteristic import Characteristic
import math
import random
from typing import List, Tuple
import logging
import Simulation.operators as operators

class Species:
    
    #Definido un diccionario caracteristicas {"caracteristica":[<valor>,<limInf>,<limSup>]} 
    def __init__(self, name):
        self.societies = 0
        self.name = name

        #En especie las características funcionan diferente de las sociedades y terrenos
        #El valor de las características dependen de los valores de cada sociedad 
        self.characteristic = {}
        self.Change_Characteristic("Poblacion", 10, 0)              #Poblacion

        logging.info("Specie %s was created", name)

    def Copy(self):
        species = Species(self.name)
        for characteristics_name in self.characteristic:
            species.characteristic[characteristics_name] = self.characteristic[characteristics_name].copy()
        return species

    def Get_Characteristic_Summation(self, name):
        return self.characteristic[name]["summation"]
    
    def z_getCharacteristicSummation(self, name):
        return self.Get_Characteristic_Summation(name)
    
    def Get_Characteristic_Mean(self, name):
        return self.characteristic[name]["mean"]

    def z_getCharacteristicMean(self, name):
        return self.Get_Characteristic_Mean(name)
    
    def Summation(self,a,b):
        return operators.default_sum(a, b)

    # Con este método podemos añadir o modificar una característica y su valor
    def Change_Characteristic(self, name, initial = 1, lower = -math.inf, upper = math.inf, mutability = -1, distr_function = None):
        if name in self.characteristic:
            dictionary= {"summation": self.characteristic[name]["summation"], "mean": self.characteristic[name]["mean"], "initial": initial, "lower": lower, "upper": upper, "mutability" : mutability, "distr_function" : distr_function}
        else:
            dictionary= {"summation": 0, "mean": 0, "initial": initial, "lower": lower, "upper": upper, "mutability" : mutability, "distr_function" : distr_function}

        self.characteristic[name] = dictionary  
        logging.info("%s has added/changed characteristic: %s with value:%s", self.name, name, dictionary)
    
    def z_changeCharacteristic(self, name, initial, lower, upper, mutability, distr_function):
        self.Change_Characteristic(name, initial, lower, upper, mutability, distr_function)
    
    def Change_Characteristic_Value(self, name, value):
        self.characteristic[name]["summation"] = self.Summation(self.characteristic[name]["summation"], value)
        if self.societies > 0:
            self.characteristic[name]["mean"] = operators.default_mul(1/self.societies, self.characteristic[name]["summation"])
        logging.info("%s has added/changed characteristic: %s with value:%s", self.name, name, value)
        
    # Con este método podemos eliminar una característica y su valor
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("%s has deleted characteristic: %s", self.name, name)
            return
        logging.warning("%s has not deleted characteristic: %s", self.name, name)
        raise Exception("Characteristic " + name + " of Species " + self.name + " doesn't exist. Cannot be deleted")

    def z_deleteCharacteristic(self, name):
        self.Delete_Characteristic(self, name)

    def Set_Default_Characteristics(self):
        self.Change_Characteristic("Mortalidad", 1)         #Mortalidad
        self.Change_Characteristic("Natalidad", 1)         #Natalidad
        self.Change_Characteristic("Esperanza de Vida", 1)        #Esperanza de vida
        self.Change_Characteristic("Gestación", 1)               #Período de Gestación
        self.Change_Characteristic("Reproducción",1) #Número de reproducción
        self.Change_Characteristic("Tamaño", 1)                    #Tamaño
        self.Change_Characteristic("Inteligencia", 1)               #Intelecto
        self.Change_Characteristic("Fuerza", 1)                #Fuerza
        self.Change_Characteristic("Capacidad de Evolución", 1)          #Capacidad de evolución
        self.Change_Characteristic("Crecimiento Actual", 1)           #Crecimiento Actual
        self.Change_Characteristic("Economía", 1)                 #Economía
        self.Change_Characteristic("Tolerancia a Extranjeros", 1)       #Tolerancia a extranjeros
        logging.info("%s has added default characteristic", self.name)

    def Change_In_Specie_Characteristic(self, characteristic, value, old_value = None):
        if characteristic in self.characteristic:
            if old_value == None:
                changed = value
            else:
                changed = operators.default_sum(value, operators.default_mul(-1,old_value))
            self.Change_Characteristic_Value(characteristic, changed)
    
