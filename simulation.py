
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
from typing import List, Tuple
import random


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
                self.map.append(Land())

        self.actual_species = [] 
        self.inter_dependences = [] # dependence_1[pos_1] -> dependence_2[pos_2] * value, lo cual se traduce como:
                                    # dependence_2[pos_2] += dependence_1[pos_1] * value


    #Método para redimensionar el mapa
    #Nota: Está incompleto, le falta eliminar las interdependencias
    #de los Land eliminados
    def Re_Dimention_Map(self, new_rows, new_columns):
        if new_rows <= 0 or new_columns <= 0:
            return 0

        new_map = []
        for i in range(new_rows):    #En cada posición de la matriz habrá un land vacío
            self.map.append([])
            for j in range(new_columns):
                if i < self.rows and j < self.columns:
                    new_map[j] = self.map[i][j]
                else:
                    new_map[j] = Land()

        self.rows = new_rows
        self.columns = new_columns
        self.map = new_map

    # Método para añadir una especie a la simulación
    def Add_Species(self, name):
        for actual in self.actual_species:
            if actual.name == name:
                return 0
        self.actual_species.append(Species(name))    


    #Método para eliminar una especie de la simulación
    def Delete_Species(self, pos):
        if pos < 0 or pos >= len(self.actual_species):
            return 0
        #Ahora debemos eliminar toda interdependencia que incluya a esta especie
        characteristics = self.actual_species[pos].characteristic.keys()
        for i in range(len(characteristics)):
            self.Delete_All_Specific_Inter_Dependence(characteristics[i], pos)
        del(self.actual_species[pos])


    #Método para cambiar las características de una especie de la simulación
    def Change_Species_Characteristic(self, pos, characteristic, value):
        return self.actual_species[pos].Change_Characteristic(characteristic, value)


    #Método para eliminar una característica de una especie de la simulación
    def Delete_Species_Characteristic(self, pos, characteristic):
        return self.actual_species[pos].Delete_Characteristic(characteristic)


    #Método para añadir una dependencia de una especie en la simulación
    def Add_Species_Dependences(self, pos, dependence_1, dependence_2, value):
        return self.actual_species[pos].Add_Dependences(dependence_1, dependence_2, value)


    #Método para eliminar una dependencia de una especie en la simulación
    def Delete_Species_Dependences(self, pos, dependence_1, dependence_2):
        return self.actual_species[pos].Delete_Dependences(dependence_1, dependence_2)


    #Método para cambiar el valor de una dependencia de una especie en la simulación
    def Change_Species_Dependences_Value(self, pos, dependence_1, dependence_2, value):
        return self.actual_species[pos].Change_Dependences_Value(dependence_1, dependence_2, value)


    #Método para cambiar las características de una terreno de la simulación
    def Change_Land_Characteristic(self, row, column, characteristic, value):
        return self.map[row][column].Change_Characteristic(characteristic, value)


    #Método para cambiar las características de un terreno de la simulación
    def Delete_Land_Characteristic(self, row, column, characteristic):
        return self.map[row][column].Delete_Characteristic(characteristic)


    #Método para añadir una dependencia de un terreno en la simulación
    def Add_Land_Dependences(self, row, column, dependence_1, dependence_2, value):
        return self.map[row][column].Add_Dependences(dependence_1, dependence_2, value)


    #Método para eliminar una dependencia de un terreno en la simulación
    def Delete_Land_Dependences(self, row, column, dependence_1, dependence_2):
        return self.map[row][column].Delete_Dependences(dependence_1, dependence_2)


    #Método para cambiar el valor de una dependencia de un terreno en la simulación
    def Change_Land_Dependences_Value(self, row, column, dependence_1, dependence_2, value):
        return self.map[row][column].Change_Dependences_Value(dependence_1, dependence_2, value)


    #Método para añadir una interdependencia
    def Add_Inter_Dependence(self, dependence_1, pos_1, dependence_2, pos_2, value):
        self.inter_dependences.append([self, dependence_1, pos_1, dependence_2, pos_2, value])



    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Change_Inter_Dependence_Value(self, dependence_1, pos_1, dependence_2, pos_2, new_value):
        for i in range(self.inter_dependences):
            dependences = self.inter_dependences[i]
            if dependence_1 in dependences and pos_1 in dependences and dependence_2 in dependences and pos_2 in dependences:
                self.inter_dependences[i][4] = new_value
                return


    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Delete_Inter_Dependence(self, dependence_1, pos_1, dependence_2, pos_2):
        for i in range(self.inter_dependences):
            dependences = self.inter_dependences[i]
            if dependence_1 in dependences and pos_1 in dependences and dependence_2 in dependences and pos_2 in dependences:
                del(self.inter_dependences[i])
                return


    #Método para eliminar todas las interdependencias que incluyan a cierto a o b
    def Delete_All_Specific_Inter_Dependence(self, inter_dependence, pos):
        for i in range(self.inter_dependences):
            dependences = self.inter_dependences[i]
            dependence_1 = dependences[0]
            pos_1 = dependences[1]
            dependence_2 = dependences[2]
            pos_2 = dependences[3]
            if (pos == pos_1 and dependence_1 == inter_dependence) or (pos == pos_2 and dependence_2 == inter_dependence):
                del(self.inter_dependences[i])


    def Set_Default_Inter_Dependences(self):
        pass


    def Move_One_Day_Inter_Dependences(self):
        
        for i in range(self.inter_dependences):

            # el inter_dependece es una lista que se guarda en el siguiente orden:
            # dependence_1[pos_1] -> dependence_2[pos_2] * value, lo cual se traduce como:
            # dependence_2[pos_2] += dependence_1[pos_1] * value

            actual_dependence = self.inter_dependences[i]    #Guardamos la dependencia actual

            #Extraemos el pos_1 y pos_2 guardados en las inter_dependences

            pos_1 = actual_dependence[1]
            pos_2 = actual_dependence[3]


            # Debemos acceder a la especie o terreno de las dependencias,
            # donde dependence_1 va a pertenecer a first y dependence_2 va a pertenecer a second
        
            first = 0
            second = 0

            # Si pos_1 o pos_2 es una lista (con dos coordenadas), entonces es un land, 
            # si es un número entonces es una especie

            if(isinstance(pos_1, List)):
                first = self.map[pos_1[0]][pos_1[0]]
            else:
                first = self.actual_species[pos_1]

            if(isinstance(pos_2, List)):
                second = self.map[pos_2[0]][pos_2[0]]
            else:
                second = self.actual_species[pos_2]


            a = first[actual_dependence[0]]            #Extraemos a
            b = first[actual_dependence[2]]            #Extraemos b
            c = actual_dependence[4]                   #Extraemos c

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

            if(isinstance(a, List)):
                a = random.randint(a[0], a[1])

            if(isinstance(b, List)):
                if(isinstance(c, List)):
                    self.characteristic[actual_dependence[1]] = [b[0] + c[0]*a, b[1] + c[1]*a]
                else:
                    self.characteristic[actual_dependence[1]] = [b[0] + c*a, b[1] + c*a]
            else:
                if(isinstance(c, List)):
                    self.characteristic[actual_dependence[1]] = b + a * random.randint(c[0], c[1])
                else:
                    self.characteristic[actual_dependence[1]] = b + a * c


    # Mueve un día de la simulación
    def Move_One_Day_All(self):
        
        for i in range(self.actual_species):
            self.actual_species[i].Move_One_Day()

        for i in range(self.rows):
            for j in range(self.columns):
                self.map[i][j].Move_One_Day()

        self.Move_One_Day_Inter_Dependences()