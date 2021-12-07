
import random
from typing import List, Tuple
import logging


class Species:

    def __init__(self, name):

        self.name = name

        #En especie las características funcionan diferente de las sociedades y terrenos
        #El valor de las características dependen de los valores de cada sociedad 
        self.characteristic = {}

        logging.info("Specie %s was created", name)


    # Con este método podemos añadir o modificar una característica y su valor
    def Change_Characteristic(self, name, method):
        self.characteristic[name] = method
        logging.info("%s has added/changed characteristic: %s with value:%s", self.name, name, method)
        

    # Con este método podemos eliminar una característica y su valor
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("%s has deleted characteristic: %s", self.name, name)
            return
        logging.warning("%s has not deleted characteristic: %s", self.name, name)

    def Set_Default_Characteristics(self):
        self.Change_Characteristic("population", 1)              #Poblacion
        self.Change_Characteristic("death_rate", [0, 1])         #Mortalidad
        self.Change_Characteristic("birth_rate", [0, 1])         #Natalidad
        self.Change_Characteristic("life_expectation", 1)        #Esperanza de vida
        self.Change_Characteristic("gestation", 1)               #Período de Gestación
        self.Change_Characteristic("reproduction_number", [0,1]) #Número de reproducción
        self.Change_Characteristic("size", 1)                    #Tamaño
        self.Change_Characteristic("intellect", 1)               #Intelecto
        self.Change_Characteristic("strength", 1)                #Fuerza
        self.Change_Characteristic("evolution_rate", 1)          #Capacidad de evolución
        self.Change_Characteristic("actual_growth", 1)           #Crecimiento Actual
        self.Change_Characteristic("economy", 1)                 #Economía
        self.Change_Characteristic("foreign_tolerance", 1)       #Tolerancia a extranjeros
        logging.info("%s has added default characteristic", self.name)
