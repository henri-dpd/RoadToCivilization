
from logging import raiseExceptions
from re import A

from numpy import sign
from Simulation.dependence import Dependence
from Simulation.characteristic import Characteristic
from asyncio.windows_events import NULL
import math


class Evolution:
    
    def __init__(self, society_name, pos, in_characteristics = []):
        self.society_name = society_name      # Nombre de la sociedad
        self.pos = pos                        #Posición de esta sociedad en simulation

        self.characteristics = []             #[[característica, valor]], con valor = 0, 1 o -1
                                              # 1 ->  Beneficia a Población
                                              # -1 -> Perjudica a Población
                                              # 0 ->  No afecta a Población

        self.inter_dependences = []       # Aquí se guardan las interdependencias que han sido descubiertas de la forma:
                                          # La pos i representa la característica afectada
                                          # La pos j representa la característica que lo afecta y se guarda como:
                                          # (entity, characteristic, value, pos), donde value es 0, 1 o -1 en dependencia,
                                          # y pos es la posición de la entidad en simulation 
                                          # de si sabemos o creemos que afecta negativa o positivamente a la característica actual
        self.values = []                  # Aquí se guardan los valores promedio actuales de cambio según las interdependencias
        self.old_values = []              # Aquí se guardan los valores promedio anteriores de cambio según las interdependencias
        self.attemps = []                 # Aquí se guardan los intentos por cambiar una interdependencia
        self.attemp_success = []          # Aquí se guarda el estado de modificación de una dependencia:
                                          # 0 - No ha podido ser modificada
                                          # 1 - Fue modificada para + o -
                                          # 2 - Fue modificada para + o - contrario al anterior
                                          # 3 - Ya fue revisada
        self.request = None               # Esta es la dependencia que lanzamos como request para evolucionar
        self.request_pos = None           # Esta es la posición de la característica a la que hace referencia el request

        for i in range(len(in_characteristics)):
            self.characteristics.append([in_characteristics[i], 0])
            self.inter_dependences.append([])
            self.values.append(0)
            self.old_values.append(0)
            self.attemps.append([])
            self.attemp_success.append([])

    #Con esto podemos añadir una característica a Evolution
    def Add_Characteristic(self, characteristic):
        pos = self.Search_Characteristic_Pos(characteristic)
        if pos != -1:
            raise Exception("El Evolution de " + self.society_name + 
                            " ya tiene la característica: " + characteristic +
                            ". Por tanto, no puede añadirla.")
        
        self.characteristics.append([characteristic, 0])
        self.inter_dependences.append([])
        self.values.append(0)
        self.old_values.append(0)
        self.attemps.append([])
        self.attemp_success.append([])

    #Con esto podemos eliminar una característica de Evolution
    def Remove_Characteristic(self, characteristic):
        pos = self.Search_Characteristic_Pos(characteristic)
        if pos == -1:
            raise Exception("El Evolution de " + self.society_name + 
                            " no tiene la característica: " + characteristic +
                            ". Por tanto no puede removerla.")
        del(self.characteristics[pos])
        del(self.inter_dependences[pos])
        del(self.values[pos])
        del(self.old_values[pos])
        del(self.attemps[pos])
        del(self.attemp_success[pos])

    #Con esto avisamos a Evolution de que el último request realizado fue aceptado
    def Request_Accepted(self):
        characteristic_1 = self.request.characteristic_1

        pos = self.request_pos

        self.attemp_success[pos[0]][pos[1]] = self.attemp_success[pos[0]][pos[1]] + 1

    #Dada una interdependencia guardamos sus datos
    def Learning_from_Interdependence(self, in_inter_dependence, value, change_value):
        #Primero obtenemos el pos de la característica que fue afectada
        pos = self.Search_Characteristic_Pos(in_inter_dependence.characteristic_2)
        if pos == -1:
            raise Exception("La característica a mejorar: " + in_inter_dependence.characteristic_2 +
                            ", no se encuentra en el Evolution de " + self.society_name)

        self.values[pos] = self.values[pos] + change_value
        
        characteristic_list = self.inter_dependences[pos]
        for dependence in characteristic_list:
            if (dependence[0] == in_inter_dependence.entity_1 and
                dependence[1] == in_inter_dependence.characteristic_1 and
                dependence[3] == in_inter_dependence.pos_1):
                return

        new_value = 0
        #En caso de que sea una dependencia de esta sociedad, podemos acceder a su value
        if(in_inter_dependence.entity_1 == self.society_name and
           in_inter_dependence.entity_2 == self.society_name and
           in_inter_dependence.pos_1 == in_inter_dependence.pos_2 and
           in_inter_dependence.pos_2 == self.pos):
            if value < 0:
                new_value = -1
            if value > 0:
                new_value = 1
            if value == 0:
                new_value = 0
        self.inter_dependences[pos].append([in_inter_dependence.entity_1, 
                                            in_inter_dependence.characteristic_1,
                                            new_value,
                                            in_inter_dependence.pos_1])
        self.attemps[pos].append(0)
        self.attemp_success[pos].append(0)

    # A partir de la lista de cambios, seleccionamos cuál request de una nueva dependencia debemos hacer
    def Request_for_Evolution(self):

        self.Check_Characteristics_Values()

        initial_request = self.Actualizate_Values() #Primero actualizamos los valores
                                                    #y verificamos si esto genera un request
        #Ahora debemos limpiar las listas de datos que usamos para el Actualizate_Values
        self.old_values = self.values
        self.values = []
        for i in range(len(self.old_values)):
            self.values.append(0)
        
        if initial_request != None:
            self.request = initial_request[0][1]
            pos = [initial_request[1][0], initial_request[1][1]]
            self.request_pos = pos
            return initial_request[0]
        #En caso de que no, entonces pasamos a seleccionar una característica para poder evolucionar
        
        positions = [] #Seleccionamos el orden de las posiciones según
                       #su prioridad, en este caso, el valor absoluto
        for i in range(len(self.characteristics)):
            positions.append((math.fabs(self.old_values[i]), i))

        positions.sort(reverse=True) #Ordenamos por valor absoluto,
                                                 #de mayor a menor
        for i in range(len(positions)): #Vamos por toda la lista
            pos = positions[i][1]     #Seleccionamos la posición actual
            if self.characteristics[pos][1] == 0: #Si no sabemos si perjudica o beneficia
                continue                          #entonces no podemos hacer nada
            else:
                dependences_list = self.inter_dependences[i] #Extraemos las dependencias que conocemos
                for j in range(len(dependences_list)):
                    #Lo siguiente es escoger alguna métrica por la que calcular cuántas veces
                    #se escoge una característica antes de detenernos y escoger otra, en este
                    #caso escogimos como métrica la cantidad de características
                    if (self.attemp_success[i][j] != 0 or self.attemps[i][j] > len(self.characteristics) or
                        (self.inter_dependences[i][j][0] == self.society_name and 
                         self.inter_dependences[i][j][2] == self.pos)):
                        continue
                    else:
                        entity_2 = self.inter_dependences[i][j][0]
                        characteristic_2 = self.inter_dependences[i][j][1]
                        pos_2 = self.inter_dependences[i][j][3]
                        entity_1 = self.society_name
                        characteristic_1 = str(self.characteristics[i][0] + "=>" + str(pos_2[0]) + "_" +
                                               str(pos_2[1]) + "_" + entity_2 + "_" + characteristic_2)
                        pos_1 = self.pos
                        c = self.characteristics[i][1] * sign(self.old_values[i])

                        self.attemps[i][j] = self.attemps[i][j] + 1
                        self.request = Dependence(pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2, c)
                        self.request_pos = [i,j]
                        return [1, self.request]
        self.Reset_values()
        return None

    #Este método para resetear los valores en base a la métrica escogida en el método anterior
    def Reset_values(self):
        for i in range(len(self.attemps)):
            dependences_list = self.attemps[i]
            for j in range(len(dependences_list)):
                if self.attemps[i][j] > len(self.characteristics):
                    self.attemps[i][j] = self.attemps[i][j] - len(self.characteristics)

    #A partir de la lista de cambios en las características analizamos las elecciones que tomamos con las nuevas
    #dependencias que generamos y reemplazamos la lista, también mandamos un request si es necesario actualizar
    #alguna de las dependencias que hemos generado
    def Actualizate_Values(self):

        for i in range(len(self.characteristics)):
            
            #En caso de que no haya habido cambios o que esté indeterminado el valor de esta posición, no hacemos nada
            if self.old_values[i] == self.values[i] or self.characteristics[i][1] == 0:
                continue

            actual_dependence_list = self.inter_dependences[i] #Accedemos a la lista de dependencias incidentes

            for j in range(len(actual_dependence_list)): #Iteramos por la lista

                #En caso de que sepamos el valor de la posición actual pero no haya seguridad todavía, lo revisamos

                if (actual_dependence_list[j][2] != 0 and self.attemp_success[i][j] > 0 and
                                                         self.attemp_success[i][j] < 3):

                    #Extraemos los datos de la interdependencia que vamos de devolver
                    entity_2 = self.inter_dependences[i][j][0]
                    characteristic_2 = self.inter_dependences[i][j][1]
                    pos_2 = self.inter_dependences[i][j][3]
                    entity_1 = self.society_name
                    characteristic_1 = str(self.characteristics[i][0] + "=>" + str(pos_2[0]) + "_" + 
                                           str(pos_2[1]) + "_" + entity_2 + "_" + characteristic_2)
                    pos_1 = self.pos

                    #Si es positivo, entonces beneficia a Población
                    if actual_dependence_list[j][2] == 1:
                        #Si mejoró el índice actual
                        if self.values[i] - self.old_values[i] > 0:
                            self.attemp_success[i][j] = 3 #Aseguramos que tomamos la decisión correcta
                            return None
                        else: #Si no, debemos cambiar la decisión
                            if self.attemp_success[i][j] == 1: #Si es la primera vez, invertimos la decisión
                                self.attemp_success[i][j] = 2
                                self.inter_dependences[i][j][2] = -1
                                return [[0, Dependence(pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2, -1)], [i,j]]
                            else: #Si es la segunda vez, eliminamos entonces la decisión tomada
                                self.attemp_success[i][j] = 3
                                self.inter_dependences[i][j][2] = 0
                                return [[-1, Dependence(pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2, 1)], [i,j]]
                    else:  #Si es negativo. entonces perjudica a la población
                        #Si diminuyó el valor, entonces debemos quedarnos con esa solución
                        if self.values[i] - self.old_values[i] < 0:
                            self.attemp_success[i][j] = 3 #Aseguramos que tomamos la decisión correcta
                            return None
                        else: #Si no, debemos cambiar la decisión
                            if self.attemp_success[i][j] == 1: #Si es la primera vez, invertimos la decisión
                                self.attemp_success[i][j] = 2
                                self.inter_dependences[i][j][2] = 1
                                return [[0, Dependence(pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2, 1)], [i,j]]
                            else: #Si es la segunda vez, eliminamos entonces la decisión tomada
                                self.attemp_success[i][j] = 3
                                self.inter_dependences[i][j][2] = 0
                                return [[-1, Dependence(pos_1, entity_1, characteristic_1, pos_2, entity_2, characteristic_2, -1)], [i,j]]
        return None

    #Método para establecer qué características afectan positiva o negativamente a la población
    def Check_Characteristics_Values(self):

        #Primero declaramos a Población como un aspecto positivo, puesto que todo lo que lo mejore o empeore
        #lo hace de forma directa
        self.characteristics[0][1] = 1

        #Primero recogemos todas las dependencias de esta sociedad a sí misma y las guardamos con su valor en una lista
        dependences_list = []
        for i in range(len(self.inter_dependences)):
            for j in range(len(self.inter_dependences[i])):
                if(self.inter_dependences[i][j][0] == self.society_name and
                   self.inter_dependences[i][j][2] == self.pos):
                    dependences_list.append((self.inter_dependences[i][j][1],
                                             self.characteristics[i][0], self.inter_dependences[i][j][2]))
        #Ahora comenzamos a recorrer este "grafo", para saber quién afecta negativa o positivamente a
        #cada característica

        #Comenzamos específicamente por Población

        positions_to_remove = []
        for i in range(len(dependences_list)):
            #Si encontramos a alguien que afecte directamente a población, guardamos los valores
            if dependences_list[i][1] == "Poblacion":
                positions_to_remove.append(i)
                pos = self.Search_Characteristic_Pos(dependences_list[i][0])
                self.characteristics[pos][1] = dependences_list[i][2]
        
        #Removemos las dependencias que usamos de la lista
        dependences_list = Remove_from_List(dependences_list, positions_to_remove)
        positions_to_remove = []

        #Lo siguiente es con la misma idea, pero con el resto de características,
        #nos detenemos cuando hemos revisado todas las depndencias y no hemos
        #elegido ninguna
        actual_change = True
        while actual_change:

            for i in range(len(dependences_list)):
                pos_2 = self.Search_Characteristic_Pos(dependences_list[i][1])
                if self.characteristics[pos_2][1] != 0:
                    pos_1 = self.Search_Characteristic_Pos(dependences_list[i][0])
                    positions_to_remove.append(i)
                    self.characteristics[pos_1][1] = self.characteristics[pos_2][1] * dependences_list[i][2]

            if len(positions_to_remove) == 0:
                actual_change = False
            else:
                dependences_list = Remove_from_List(dependences_list, positions_to_remove)
                positions_to_remove = []

    def Search_Characteristic_Pos(self, characteristic):
        for i in range(len(self.characteristics)):
            if(characteristic == self.characteristics[i][0]):
                return i
        return -1
    
# Dada una lista de elementos, y una lista de posiciones, remueve todos los elementos de la primera lista
# que correspondan a esas posiciones
def Remove_from_List(list, positions_to_remove):
    positions_to_remove.sort()
    count = 0
    for i in positions_to_remove:
        count = count + 1
        del(list[i - count])
    return list

