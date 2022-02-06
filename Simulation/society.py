import random
from typing import List, Tuple
import logging
import math

from pathlib import Path
from sys import path

path.append(str(Path(__file__).parent.parent.absolute()))

from Simulation.characteristic import Characteristic
from Simulation.evolution import Evolution
import Simulation.operators as operators


class Society:
    #Definido nombre y especie
    #Definido un diccionario caracteristicas {"caracteristica":[<valor>,<limInf>,<limSup>]} 
    def __init__(self, name, species, pos = None):

        self.name = name
        species.societies = species.societies + 1
        self.species = species
        self.pos = pos

        self.characteristic = {}
        self.enable_evolution = True
        self.evolution = Evolution(self.name, self.pos)
        for char in species.characteristic:
            self.Change_Characteristic(char, species.characteristic[char]["initial"],species.characteristic[char]["lower"], species.characteristic[char]["upper"], species.characteristic[char]["mutability"], species.characteristic[char]["distr_function"])
        logging.info("Society was created")

    #Permite habilitar la clase Evolución en esta Sociedad
    def Start_Evolution(self, pos = None):
        self.enable_evolution = True
        if pos == None:
            self.evolution = Evolution(self.name, self.pos, self.characteristic)
        else:
            self.evolution = Evolution(self.name, pos, self.characteristic)

    #Permite deshabilitar la clase Evolución en esta sociedad
    def Disable_Evolution(self):
        self.enable_evolution = False

    def Learning_for_Evolution(self, in_inter_dependence, value, change_value):
        if self.enable_evolution:
            self.evolution.Learning_from_Interdependence(in_inter_dependence, value, change_value)

    def Request_for_Evolution(self):
        if self.enable_evolution:
            return self.evolution.Request_for_Evolution()

    def Request_from_Land(self, value, inter_dependence, node_value = 0):
        if value == 1:
            self.Change_Characteristic(inter_dependence.characteristic_1, node_value)
            self.evolution.Request_Accepted()
        else:
            self.Delete_Characteristic(inter_dependence.characteristic_1)

    #Toma el valor de la caracteristica de entrada
    def Get_Characteristic_Value(self, characteristic_name):
        if characteristic_name in self.characteristic:
            return self.characteristic[characteristic_name].value
        else:
            raise Exception("La característica " + characteristic_name + 
                            " no se encuentra en la sociedad " + self.name)

    def z_getCharacteristic(self,name):
        return self.Get_Characteristic_Value(name)

    # Con este método podemos añadir o modificar el valor de una característica
    # lower limite inferior, upper  limite superior
    def Change_Characteristic(self, name, value, lower = -math.inf, upper = math.inf, mutability = -1, distr_function = None):
        if name in self.characteristic:
            old_value = self.characteristic[name].value
            self.characteristic[name].Change_Characteristic(name, value, lower, upper, mutability, distr_function)
            new_value = self.characteristic[name].value
            self.species.Change_In_Specie_Characteristic(name, new_value, old_value)
        else:
            if mutability == -1:
                mutability = 5
            if distr_function == None:
                distr_function = operators.distribution_default
            self.characteristic[name] = Characteristic(name, value, lower, upper, mutability, distr_function)
            self.species.Change_In_Specie_Characteristic(name, self.characteristic[name].value)
            self.evolution.Add_Characteristic(name)

    def z_changeCharacteristic(self, name, value, lower, upper, mutability, distr_function):
        if len(value) ==1:
            self.Change_Characteristic(name, value[0], lower, upper, mutability, distr_function)
        elif len(value) == 2:
            self.Change_Characteristic(name, value, lower, upper, mutability, distr_function)
    
    def Delete(self):
        for charac in self.characteristic:
            self.Change_Characteristic(charac, 0)
        self.species.societies = self.species.societies - 1

    # Con este método podemos eliminar una característica
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            self.evolution.Remove_Characteristic(name)
            logging.info("Society has deleted characteristic: %s", name)
            return
        logging.warning("Society has not deleted characteristic: %s", name)
        raise Exception("Sociedad " + self.name + " of Land " + str(self.pos) + " doesn't has characteristic " + name +
                        ". Cannot be removed")

    def z_deleteCharacteristic(self, name):
        self.Delete_Characteristic(name)

    #Actualiza el valor de una caracteristica existente, tomando el mismo lower y upper
    def Update_Characteristic_Value(self, name, value):
        if name in self.characteristic:
            self.characteristic[name].Update_Characteristic_Value(value)

    def Enable_Evolution(self, value : bool):
        self.enable_evolution = value

    def Copy(self, new_species):
        copy_society = Society(self.name, new_species, self.pos)
        if self.enable_evolution:
            copy_society.Enable_Evolution(True)
        return copy_society

    #Pone caracteristicas por defecto
    def Set_Default_Characteristics(self):        
        self.Change_Characteristic("Mortalidad", [0, 1], 0)
        self.Change_Characteristic("Natalidad", [0, 1], 0)
        self.Change_Characteristic("Esperanza de Vida", 1, 0)
        self.Change_Characteristic("Gestación", 1, 0)
        self.Change_Characteristic("Reproducción", [0,1], 0)
        self.Change_Characteristic("Tamaño", 1, 0)
        self.Change_Characteristic("Inteligencia", 1, 0)
        self.Change_Characteristic("Fuerza", 1, 0)
        self.Change_Characteristic("Capacidad de Evolución", 1)
        self.Change_Characteristic("Crecimiento Actual", 1)
        self.Change_Characteristic("Economía", 1)
        self.Change_Characteristic("Tolerancia a Extranjeros", 1)
        logging.info("Society has added default characteristic")
