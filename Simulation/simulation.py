
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
from typing import List, Tuple
import random
import logging
import math

from numpy import character

path.append(Path(__file__).parent.absolute())

from Simulation.dependence import Dependence
from Simulation.species import Species
from Simulation.land import Land
from Simulation.evolution import Remove_from_List
import Simulation.operators as operators

class Simulation:
    #Definido filas y columnas, y creado el mapa que no es mas que una lista de listas de terrenos
    #Definido un diccionario actual especies {"especies": especies} 
    #Definido una lista inter-dependencias [<entidad_1>,<caracteristica_A>,<entidad_2>,<caracteristica_B>,<valor>] 
    #Definido un diccionario operadores {"operador": funcion} para calcular dependencias, influencias u otro proceso que describa el usuario 
    #Definido un diccionario distribuciones {"distribucion": funcion} para calcular un valor en un rango de acuerdo a la distribucion establecida
    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns

        self.map = []

        for i in range(rows):    #En cada posición de la matriz habrá un land vacío
            self.map.append([])
            for j in range(columns):
                self.map[i].append(Land([i,j]))

        self.actual_species = {}
        self.inter_dependences = [] # dependence_1[pos_1] -> dependence_2[pos_2] * value, lo cual se traduce como:
                                    # dependence_2[pos_2] += dependence_1[pos_1] * value
                                  
        
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
                    new_map[i].append(Land([i,j]))

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
            

    # Método para añadir una especies a la simulación
    def Add_Species(self, name):
        if name in self.actual_species:
            logging.warning("Species %s alredy exists", name)
            return 0
        self.actual_species[name] = Species(name)
        logging.info("Species %s has added", name)

    def Add_Species_Copy(self, species):
        if species.name in self.actual_species:
            raise Exception("The Species " + species.name + " are already in Simulation. Cannot be added again")
        self.actual_species[species.name] = species.Copy()


    #Método para eliminar una especies de la simulación
    def Delete_Species(self, name):
        if not name in self.actual_species:
            logging.info("Species %s was not exist", name)
            return
        for i in range(self.rows):
            for j in range(self.columns):
                for society in self.map[i][j].entities:
                    if society == '':
                        continue
                    if self.map[i][j].entities[society].species == name:
                        for dependence in self.map[i][j].entities[society].characteristic:
                            self.Delete_All_Specific_Inter_Dependence([i,j], society, dependence)
                        self.map[i][j].Delete_Society(society)
        #Falta trabajar interdependencias
        del(self.actual_species[name])
        logging.info("Species %s was deleted", name)

    #Método para cambiar las características de una especies de la simulación
    def Change_Species_Characteristic(self, pos, characteristic, value, lower = -math.inf, upper = math.inf, mutability = -1, distr_function = None):
        return self.actual_species[pos].Change_Characteristic(characteristic, value, lower, upper, mutability, distr_function)


    #Método para eliminar una característica de una especies de la simulación
    def Delete_Species_Characteristic(self, pos, characteristic):
        return self.actual_species[pos].Delete_Characteristic(characteristic)


    #Para la especies del nombre de la entrada busca todas las sociedades y le pone las caraceristicas por defecto
    def Set_Default_Species_Characteristic(self, name):
        self.actual_species[name].Set_Default_Characteristics()
        for i in range(self.rows):
            for j in range(self.columns):
                for society in self.map[i][j].entities:
                    if society == '':
                        continue
                    if self.map[i][j].entities[society].species == name:
                        self.map[i][j].Set_Default_Entities_Characteristic(society)

    #Añadir sociedad a la lista de entidades, crea una sociedad con el nombre y especie de entrada        
    def Add_Society(self, row, column, name, species_name):
        return self.map[row][column].Add_Society(name, self.actual_species[species_name])

    def Add_Society_Copy(self, society, row, column):
        land = self.map[row][column]
        if society.name in land.entities:
            raise Exception("The society " + society.name + " are already in the Land " + row + "," + column +
                            ". Cannot be added")
        if not society.species.name in self.actual_species:
            raise Exception("The society " + society.name + " has an unknown species: " + society.species.name)
        else:
            copy_society = society.copy(self.actual_species[society.species.name])
            self.map[row][column].entities[copy_society.name] = copy_society
            


    #Eliminar sociedad de nombre de la entrada
    def Delete_Society(self, row, column, name):
        remove_list = []
        for i in range(len(self.inter_dependences)):
            if ((self.inter_dependences[i].entity_1 == name and [row, column] == self.inter_dependences[i].pos_1) or
                (self.inter_dependences[i].entity_2 == name and [row, column] == self.inter_dependences[i].pos_2)):
                remove_list.append(i)
        self.inter_dependences = Remove_from_List(self.inter_dependences, remove_list)
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

    #Método para resetear un Land
    def Reset_Land(self, row, column):
        remove_list = []
        for i in range(len(self.inter_dependences)):
            if ([row, column] == self.inter_dependences[i].pos_1 or [row, column] == self.inter_dependences[i].pos_2):
                remove_list.append(i)
        self.inter_dependences = Remove_from_List(self.inter_dependences, remove_list)
        for entity in self.map[row][column].entities:
            self.Delete_Society(row, column, entity)
            self.map[row][column].characteristic = {}

    #Método para agregar un copia de un Land a la Simulación
    def Add_Land_Copy(self, land, row, column):
        self.Reset_Land(row, column)
        self.map[row][column].Copy(land)

    #Método para cambiar las características de una terreno de la simulación
    def Change_Land_Characteristic(self, row, column, characteristic, value, lower = -math.inf, upper = math.inf, mutability = -1, distr_function = None):
        return self.map[row][column].Change_Characteristic(characteristic, value, lower, upper, mutability, distr_function)

    #Método para cambiar las características de un terreno de la simulación
    def Delete_Land_Characteristic(self, row, column, characteristic):
        remove_list = []
        for i in range(len(self.inter_dependences)):
            if ((self.inter_dependences[i].characteristic_1 == characteristic and [row, column] == self.inter_dependences[i].pos_1) or
                (self.inter_dependences[i].characteristic_2 == characteristic and [row, column] == self.inter_dependences[i].pos_2)):
                remove_list.append(i)
        self.inter_dependences = Remove_from_List(self.inter_dependences, remove_list)
        return self.map[row][column].Delete_Characteristic(characteristic)

    #Método para actualizar las características de un terreno de la simulación
    def Update_Land_Characteristic_Value(self,  row, column, characteristic, value):
        return self.map[row][column].Update_Characteristic_Value(characteristic, value)
    
    
    #Método para añadir una dependencia de un terreno en la simulación
    def Add_Land_Dependences(self, row, column, entity_1, dependence_1, entity_2, dependence_2, value, sum = None, mul = None):
        return self.map[row][column].Add_Dependence(entity_1, dependence_1, entity_2, dependence_2, value, sum, mul)


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
    def Add_Inter_Dependence(self, pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, value, sum = None, mul = None):
        if((not entity_1 in self.map[pos_1[0]][pos_1[1]].entities) or
           (not entity_2 in self.map[pos_2[0]][pos_2[1]].entities) or
           (not dependence_1 in self.map[pos_1[0]][pos_1[1]].entities[entity_1].characteristic) or
           (not dependence_2 in self.map[pos_2[0]][pos_2[1]].entities[entity_2].characteristic)):
            raise Exception("Interdependence [" + pos_1 + ", " + entity_1 + ", " + dependence_1 + ", " +  pos_2 + ", " + 
                                 entity_2 + ", " + dependence_2 + " has at least one parameter that doesn't exists in the Simulation.")
        inter = Dependence(pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, value, sum, mul)
        for interdependence in self.inter_dependences:
            if interdependence.IsInstance(inter):
                logging.warning("interdependence was not added: interdependence alredy exists")
                raise Exception("Interdependence [" + pos_1 + ", " + entity_1 + ", " + dependence_1 + ", " +  pos_2 + ", " + 
                                 entity_2 + ", " + dependence_2 + " was added twice.")
                return
        if pos_1 != pos_2:
            self.inter_dependences.append(inter)
        else:
            self.map[pos_1[0]][pos_2[1]].Add_Dependence(entity_1, dependence_1, entity_2, dependence_2, value, sum, mul)
        logging.info("interdependence was added")


    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Change_Inter_Dependence_Value(self, pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, new_value):
        inter = Dependence(pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, new_value)
        for interdependence, i in enumerate(self.inter_dependences):
            if interdependence.IsInstance(inter):
                self.inter_dependences[i].Change_C(new_value)
                logging.info("Interdependence was changed")
                return
        logging.warning("Interdependence was not changed: interdependence does not exist")


    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Delete_Inter_Dependence(self, pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2):
        if pos_1 == pos_2:
            self.map[pos_1[0]][pos_1[1]].Delete_Dependence(entity_1, dependence_1, entity_2, dependence_2)
        else:
            inter = Dependence(pos_1, entity_1, dependence_1, pos_2, entity_2, dependence_2, 0)
            for interdependence, i in enumerate(self.inter_dependences):
                if interdependence.IsInstance(inter):
                    del(self.inter_dependences[i])
                    logging.info("Interdependence was deleted")
                    return
        logging.warning("Interdependence was not deleted: interdependence does not exist")
                

    #Método para eliminar todas las interdependencias que incluyan a cierto a o b
    def Delete_All_Specific_Inter_Dependence(self, pos, entity, dependence):
        for interdependence, i in enumerate(self.inter_dependences):
            if interdependence.Is_In((pos, entity, dependence)):
                del(self.inter_dependences[i])
                logging.info("Interdependence was deleted")
                

    #Ejecuta todas las interdependencias
    def Move_One_Day_Inter_Dependences(self):                
        actual_status={}
        for actual_dependence in self.inter_dependences:
            # el inter_dependece es una lista que se guarda en el siguiente orden:
            # dependence_1[pos_1] -> dependence_2[pos_2] * value, lo cual se traduce como:
            # dependence_2[pos_2] += dependence_1[pos_1] * value

            #Extraemos el pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2 guardados en las inter_dependences
            pos_1 = actual_dependence.pos_1
            entity_1  = actual_dependence.entity_1
            characteristic_1  = actual_dependence.characteristic_1
            pos_2 = actual_dependence.pos_2
            entity_2  = actual_dependence.entity_2
            characteristic_2  = actual_dependence.characteristic_2
            plus  = actual_dependence.plus_function
            mult  = actual_dependence.mult_function

            #Extraemos a, b, c
            distribution = self.map[pos_1[0]][pos_1[1]].entities[entity_1].characteristic[characteristic_1].distr_function
            a = distribution(self.map[pos_1[0]][pos_1[1]].Get_Entities_Characteristic_value(entity_1, characteristic_1))
            b = self.map[pos_2[0]][pos_2[1]].Get_Entities_Characteristic_value(entity_2, characteristic_2)
            c = actual_dependence.c

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

            result = operators.dependence(plus, mult)(a, b, c)
            actual_status[(pos_2[0], pos_2[1], entity_2, characteristic_2)] = result
            
            change_value=0
            if isinstance(b,List):
                change_value = (result[0] - b[0] + result[1] - b[1])/2
            else:
                change_value = result - b
            self.Learning_for_Evolution(actual_dependence, a, change_value)

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

        #Luego le damos a las sociedades la oportunidad de evolucionar
        self.Request_for_Evolution()
        
        to_delete = []
        for i in range(self.rows):
            for j in range(self.columns):
                for entity in self.map[i][j].entities:
                    if entity != '' and self.map[i][j].entities[entity].characteristic["Población"].value <=0:
                        to_delete.append([i,j,entity])
        for i,j,entity in to_delete:
            self.Delete_Society(i,j,entity)

        #El orden de avance del día visto anteriormente se toma por conveniencia
        logging.info("Simulations was move one day")

    #Permite habilitar la clase Evolución para alguna de las sociedades
    def Start_Evolution(self, pos, society_name):
        self.map[pos[0]][pos[1]].Start_Evolution(society_name)

    def Learning_for_Evolution(self, in_inter_dependence, value, change_value):
        pos = in_inter_dependence.pos_2
        self.map[pos[0]][pos[1]].Learning_for_Evolution(in_inter_dependence, value, change_value)

    #Hace avanzar el algoritmo de evolución en todos los land
    def Request_for_Evolution(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                land_dependences_request = self.map[i][j].Request_for_Evolution()
                for k in range(len(land_dependences_request)):
                    self.Request_From_Land_One(land_dependences_request[k][0], land_dependences_request[k][1])

    #Recibe un request de alguna society en algún land para evolucionar
    def Request_From_Land_One(self, value, inter_dependence):
        entity_2 = inter_dependence.entity_2
        characteristic_2 = inter_dependence.characteristic_2

        pos_2 = inter_dependence.pos_2

        if value == 1:
            mutability = self.map[pos_2[0]][pos_2[1]].entities[entity_2].characteristic[characteristic_2].mutability
            if operators.distribution_default([0, 10]) > mutability:
                modify_value = operators.distribution_default([5, 20])
                node_value = self.map[pos_2[0]][pos_2[1]].Get_Entities_Characteristic_value(inter_dependence.entity_2, inter_dependence.characteristic_2) * modify_value / 100

                pos_1 = inter_dependence.pos_1
                
                self.map[pos_1[0]][pos_1[1]].Request_From_Simulation(value, inter_dependence, node_value)

                self.Add_Inter_Dependence(pos_1, inter_dependence.entity_1, inter_dependence.characteristic_1,
                                          pos_2, inter_dependence.entity_2, inter_dependence.characteristic_2,
                                          inter_dependence.c)
                

        if value == 0:
            self.Change_Inter_Dependence_Value(pos_1, inter_dependence.entity_1, inter_dependence.characteristic_1,
                                               pos_2, inter_dependence.entity_2, inter_dependence.characteristic_2,
                                               inter_dependence.c)
        if value == -1:
            self.Delete_Inter_Dependence(pos_1, inter_dependence.entity_1, inter_dependence.characteristic_1,
                                         pos_2, inter_dependence.entity_2, inter_dependence.characteristic_2)
            self.map[pos_1[0]][pos_1[1]].Request_From_Simulation(value, inter_dependence)
    
    
    def Set_Default_Inter_Dependences(self):
        pass