
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
from typing import List, Tuple
import random
import logging
import math

path.append(Path(__file__).parent.absolute())

from species import Species
from land import Land

class Simulation:

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns

        self.map = []

        for i in range(rows):    #En cada posición de la matriz habrá un land vacío
            self.map.append([])
            for j in range(columns):
                self.map[i].append(Land())

        self.actual_species = {}
        self.inter_dependences = [] # dependence_1[pos_1] -> dependence_2[pos_2] * value, lo cual se traduce como:
                                    # dependence_2[pos_2] += dependence_1[pos_1] * value
        
        self.operators = {
            "dependence": (lambda a, b, c : self.sum(b, self.mul(a, c))),
            "influence": (lambda old_a, act_a, b, c : self.sum(b, self.mul(self.sum(act_a, self.mul(old_a, -1)), c))),
            #"limit": (lambda a, b, c : b if b < self.mul(a, c) else self.mul(a, c)),
            }
        self.distributions = {
            "default": lambda c: random.randint(round(c[0]), round(c[1])) if isinstance(c, List) else c
        }                            
        
        logging.info("Simulation was created")


    #Método para redimensionar el mapa
    def Re_Dimention_Map(self, new_rows, new_columns):
        if new_rows <= 0 or new_columns <= 0:
            return 0

        new_map = []
        for i in range(new_rows):    #En cada posición de la matriz habrá un land vacío
            new_map.append([])
            for j in range(new_columns):
                if i < self.rows and j < self.columns:
                    new_map[i].append(self.map[i][j])
                else:
                    new_map[i].append(Land())

        self.rows = new_rows
        self.columns = new_columns
        self.map = new_map
        
        #Eliminar interdependencias de terrenos perdidos en la redimensión del mapa
        for interdependence, i in enumerate(self.inter_dependences):
            pos_1 = interdependence[1]
            pos_2 = interdependence[3]
            if isinstance(pos_1, List):
                if pos_1[0]>=new_rows or pos_1[1]>=new_columns:
                    del(self.inter_dependences[i])
            if isinstance(pos_2, List):
                if pos_2[0]>=new_rows or pos_2[1]>=new_columns:
                    del(self.inter_dependences[i])
        logging.info("Map was resized: %s rows, %s columns", new_rows, new_columns)
            
        

    # Método para añadir una especie a la simulación
    def Add_Species(self, name):
        if name in self.actual_species:
            logging.warning("Specie %s alredy exists", name)
            return 0
        self.actual_species[name] = Species(name)
        logging.info("Specie %s has added", name) 


    #Método para eliminar una especie de la simulación
    def Delete_Species(self, name):
        if not name in self.actual_species:
            logging.info("Specie %s was not exist", name)
            return
        for i in range(self.rows):
            for j in range(self.columns):
                for society in self.map[i][j].entities:
                    if society == '':
                        continue
                    if self.map[i][j].entities[society].specie == name:
                        for dependence in self.map[i][j].entities[society].characteristic:
                            del(self.inter_dependences[[i,j], society, dependence])
                        del(self.map[i][j].entities[society])
        #Falta trabajar interdependencias
        del(self.actual_species[name])
        logging.info("Specie %s was deleted", name)


    #Método para cambiar las características de una especie de la simulación
    def Change_Species_Characteristic(self, pos, characteristic, method):
        return self.actual_species[pos].Change_Characteristic(characteristic, method)


    #Método para eliminar una característica de una especie de la simulación
    def Delete_Species_Characteristic(self, pos, characteristic):
        return self.actual_species[pos].Delete_Characteristic(characteristic)


    def Set_Default_Species_Characteristic(self, name):
        self.actual_species[name].Set_Default_Characteristics()
        for i in range(self.rows):
            for j in range(self.columns):
                for society in self.map[i][j].entities:
                    if society == '':
                        continue
                    if self.map[i][j].entities[society].specie == name:
                        self.map[i][j].Set_Default_Entities_Characteristic(society)


     #Añadir sociedad a la lista de entidades, crea una sociedad con el nombre y especie de entrada 
    def Add_Society(self, row, column, name, specie):
        return self.map[row][column].Add_Society(name, specie)

    #Eliminar sociedad de nombre de la entrada
    def Delete_Society(self, row, column, name):
        return self.map[row][column].Delete_Society(name)


    #Método para cambiar las características de una sociedad en un terreno de la simulación
    def Change_Society_Characteristic(self, row, column, name, characteristic, value, lower = -math.inf, upper = math.inf):
        return self.map[row][column].Change_Entities_Characteristic(name, characteristic, value, lower, upper)

    #Método para cambiar las características de una sociedad en un terreno de la simulación
    def Delete_Society_Characteristic(self, row, column, name, characteristic):
        return self.map[row][column].Delete_Characteristic(name, characteristic)

    #Método para actualizar las características de una sociedad en un terreno de la simulación
    def Update_Society_Characteristic_Value(self,  row, column, name, characteristic, value):
        return self.map[row][column].Update_Characteristic_Value(name, characteristic, value)
    

    #Método para cambiar las características de una terreno de la simulación
    def Change_Land_Characteristic(self, row, column, characteristic, value, lower = -math.inf, upper = math.inf):
        return self.map[row][column].Change_Characteristic(characteristic, value, lower, upper)

    #Método para cambiar las características de un terreno de la simulación
    def Delete_Land_Characteristic(self, row, column, characteristic):
        return self.map[row][column].Delete_Characteristic(characteristic)

    #Método para actualizar las características de un terreno de la simulación
    def Update_Land_Characteristic_Value(self,  row, column, characteristic, value):
        return self.map[row][column].Update_Characteristic_Value(characteristic, value)
    
    
    #Método para añadir una dependencia de un terreno en la simulación
    def Add_Land_Dependences(self, row, column, entity_1, dependence_1, entity_2, dependence_2, value):
        return self.map[row][column].Add_Dependence(entity_1, dependence_1, entity_2, dependence_2, value)


    #Método para eliminar una dependencia de un terreno en la simulación
    def Delete_Land_Dependences(self, row, column, entity_1, dependence_1, entity_2, dependence_2):
        return self.map[row][column].Delete_Dependences(entity_1, dependence_1, entity_2, dependence_2)


    #Método para cambiar el valor de una dependencia de un terreno en la simulación
    def Change_Land_Dependences_Value(self, row, column, entity_1, dependence_1, entity_2, dependence_2, value):
        return self.map[row][column].Change_Dependences_Value(entity_1, dependence_1, entity_2, dependence_2, value)


    #Método para añadir una influencia de un terreno en la simulación
    def Add_Land_Influences(self, row, column, entity_1, dependence_1, entity_2, dependence_2, value):
        return self.map[row][column].Add_Influences(entity_1, dependence_1, entity_2, dependence_2, value)


    #Método para eliminar una influencia de un terreno en la simulación
    def Delete_Land_Influences(self, row, column, entity_1, dependence_1, entity_2, dependence_2):
        return self.map[row][column].Delete_Influences(entity_1, dependence_1, entity_2, dependence_2)


    #Método para cambiar el valor de una influencia de un terreno en la simulación
    def Change_Land_Influences_Value(self, row, column, entity_1, dependence_1, entity_2, dependence_2, value):
        return self.map[row][column].Change_Influences_Value(entity_1, dependence_1, entity_2, dependence_2, value)


    def Set_Default_Land_Characteristic(self, row, column):
        return self.map[row][column].Set_Default_Characteristics()


    #Método para añadir una interdependencia
    def Add_Inter_Dependence(self, pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, value):
        if (not entity_1 in self.map[pos_1[0]][pos_1[1]].entities) or (not entity_2 in self.map[pos_2[0]][pos_2[1]].entities):
            return
        self.inter_dependences.append([(pos_1, entity_1, dependence_1),( pos_2, entity_2, dependence_2), value])
        logging.info("interdependence was added")


    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Change_Inter_Dependence_Value(self, pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, new_value):
        for dependences, i in enumerate(self.inter_dependences):
            if (pos_1, entity_1, dependence_1) == dependences[0] and (pos_2, entity_2, dependence_2) == dependences[1]:
                self.inter_dependences[i][2] = new_value
                logging.info("Interdependence was changed")
                return
        logging.warning("Interdependence was not changed: interdependence does not exist")


    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Delete_Inter_Dependence(self, pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2):
        for dependences, i in enumerate(self.inter_dependences):
            if (pos_1, entity_1, dependence_1) == dependences[0] and (pos_2, entity_2, dependence_2) == dependences[1]:
                del(self.inter_dependences[i])
                logging.info("Interdependence was deleted")
                return
        logging.warning("Interdependence was not deleted: interdependence does not exist")
                

    #Método para eliminar todas las interdependencias que incluyan a cierto a o b
    def Delete_All_Specific_Inter_Dependence(self, pos, entity, dependence):
        for dependences, i in enumerate(self.inter_dependences):
            if (pos, entity, dependence) in dependences:
                del(self.inter_dependences[i])
                logging.info("Interdependence was deleted")
                

    def Set_Default_Inter_Dependences(self):
        pass


    #nuestras operaciones para operar con rangos o valores numericos 
    def sum(self,a, b):
        if isinstance(a,List):
            if isinstance(b,List):
                return [a[0] + b[0], a[1] + b[1]]
            return [a[0] + b, a[1] + b]
        return a + self.distributions["default"](b)

    def mul(self,a, b):
        if isinstance(b,List):
            return [b[0] * a, b[1] * a]
        return a * b
    
    def comp(self, a, b):
        if isinstance(a,List) and isinstance(a,List):
            return a[0] > b[0] and a[1] < b[1] 
        return a * b
 

    def Move_One_Day_Inter_Dependences(self):                
        actual_status={}
        for actual_dependence in self.inter_dependences:
            # el inter_dependece es una lista que se guarda en el siguiente orden:
            # dependence_1[pos_1] -> dependence_2[pos_2] * value, lo cual se traduce como:
            # dependence_2[pos_2] += dependence_1[pos_1] * value

            #Extraemos el pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2 guardados en las inter_dependences
            pos_1 = actual_dependence[0][0]
            entity_1  = actual_dependence[0][1]
            characteristic_1  = actual_dependence[0][2]
            pos_2 = actual_dependence[1][0]
            entity_2  = actual_dependence[1][1]
            characteristic_2  = actual_dependence[1][2]

            #Extraemos a, b, c
            a = self.distributions["default"](self.map[pos_1[0]][pos_1[1]].Get_Entities_Characteristic_value(entity_1, characteristic_1))
            b = self.map[pos_2[0]][pos_2[1]].Get_Entities_Characteristic_value(entity_2, characteristic_2)
            c = actual_dependence[2] 

            #Aquí se hace una separación por casos:
            #Si a tiene dos coordenadas, entonces el valor de a es directamente un random de ese intervalo
            #Si a es un valor, entonces a es directamente igual a ese valor
            #Ya sea que b tiene un valor, o dos coordenadas, estos no se verifican mediante un random, sino que
            #se multiplican a partir de los casos de c:

            #Si b es un valor y c una coordenada, entonces a se multiplica por un random proporcionado por el intervalo de c
            #Si b es un valor y c un valor, se multiplican
            #Si b es una coordenada (b1, b2), y c una coordenada (c1, c2), entonces se debe hacer:
            # (b1, b2) = (b1, b2) + (c1*a, c2*a)
            #Si b es una coordenada y c un valor entonces se multiplica ambas a por c

            actual_status[(pos_2[0], pos_2[1], entity_2, characteristic_2)] = self.operators["dependence"](a, b, c)
            logging.info("Simulation has update characteristic with interdependence")
        
        #Los cambios finales resultantes de las dependencias e influencias actualizan las caracteristicas modificadas
        for update in actual_status:
            self.map[update[0]][update[1]].Update_Entities_Characteristic(update[2], update[3], actual_status[update])        
        logging.info("Land has move one day")
        logging.info("Simulations interdependences was move one day")



    # Mueve un día de la simulación
    def Move_One_Day_All(self):
        #Avanza un día en cada terreno
        for i in range(self.rows):
            for j in range(self.columns):
                (self.map[i][j]).Move_One_Day()
        logging.info("Simulations map was move one day")

        #Luego avanzan las interdependencias entre terrenos
        self.Move_One_Day_Inter_Dependences()

        #El orden de avance del día visto anteriormente se toma por conveniencia
        logging.info("Simulations was move one day")