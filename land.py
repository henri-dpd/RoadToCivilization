import random
from typing import List, Tuple
import logging
import math

from society import Society


class Land:

    def __init__(self):

        self.characteristic = {}
        self.characteristic_dependences = [] # dependence_1 -> dependence_2 * value
        self.characteristic_influences = [] # influence_1 -> influence_2 * value
        #self.characteristic_limits = [] # limit_1 -> limit_2 * value
        self.societies = {} # Diccionario de sociedades{ especie: Sociedad}
        self.inter_dependences = [] # interpedendencias espedie terreno, especie especie
        self.operators = {
            "dependence": (lambda a, b, c : self.sum(b, self.mul(a, c))),
            "influence": (lambda old_a, act_a, b, c : self.sum(b, self.mul(self.sum(act_a, self.mul(old_a, -1)), c)))
            }
        self.distribitions = {
            "default": lambda c: random.randint(round(c[0]), round(c[1])) if isinstance(c, List) else c
        }
        
        logging.info("Land was created")

    def Add_Society(self, name, specie):
        for society in self.societies:
            if society == name:
                logging.warning("Society %s alredy exists", name)
                return False
        self.societies[name] = Society(name, specie)
        logging.info("Society %s was added", name)
        
    def Delete_Society(self, name):
        if name not in self.societies.keys():
            logging.warning("Society was not added: Society do not exists")
            return 0
        #Ahora debemos eliminar toda interdependencia que incluya a esta especie
        for characteristic in self.societies[name].characteristic:
            self.Delete_All_Specific_Inter_Dependence(characteristic, name)
        del(self.societies[name])
        logging.info("Society %s was deleted", name)

    #Método para cambiar las características de una especie de la simulación
    def Change_Societies_Characteristic(self, name, characteristic, value):
        return self.societies[name].Change_Characteristic(characteristic, value)

    #Método para eliminar una característica de una especie de la simulación
    def Delete_Societies_Characteristic(self, name, characteristic):
        return self.societies[name].Delete_Characteristic(characteristic)

    #Método para añadir una dependencia de una especie en la simulación
    def Add_Societies_Dependences(self, name, dependence_1, dependence_2, value):
        return self.societies[name].Add_Dependences(dependence_1, dependence_2, value)

    #Método para eliminar una dependencia de una especie en la simulación
    def Delete_Societies_Dependences(self, name, dependence_1, dependence_2):
        return self.societies[name].Delete_Dependences(dependence_1, dependence_2)

    #Método para cambiar el valor de una dependencia de una especie en la simulación
    def Change_Societies_Dependences_Value(self, name, dependence_1, dependence_2, value):
        return self.societies[name].Change_Dependences_Value(dependence_1, dependence_2, value)

    def Set_Default_Societies_Characteristic(self, name):
        return self.societies[name].Set_Default_Characteristics()


    def Get_Characteristic_Value(self, name):
        return self.characteristic[name][0]

    # Con este método podemos añadir o modificar una característica y su valor
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
        logging.info("Land has added/changed characteristic: %s with value:%s", name, value)

    # Con este método podemos eliminar una característica y su valor
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("Land has deleted characteristic: %s", name)
            for i, dependence in enumerate(self.characteristic_dependences):
                if name in dependence:
                    del(dependence[i])
            return
        logging.warning("Land has not deleted characteristic: %s", name)

    def Update_Characteristic_Value(self, name, value):
        lower = self.characteristic[name][1]
        upper = self.characteristic[name][2]
        self.Change_Characteristic(name, value, lower, upper) 
    
    # Con este método podemos agregar una dependencia de la forma a -> b * c
    # Donde a es dependence_1, b es dependence_2 y c es value
    def Add_Dependences(self, dependence_1, dependence_2, value):
        for dependences in self.characteristic_dependences:      #Revisamos que no exista esta dependencia
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                logging.warning("Land has not added dependece: %s -> %s * %s", dependence_1, dependence_2, value)
                return 0    #Si existe devolvemos 0
        self.characteristic_dependences.append([dependence_1, dependence_2, value]) #Agregamos la dependencia
        logging.info("Land has added dependece: %s -> %s * %s", dependence_1, dependence_2, value)

    # Con este método podemos eliinar una dependencia
    def Delete_Dependences(self, dependence_1, dependence_2):
        for i, dependences in enumerate(self.characteristic_dependences):
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                del(self.characteristic_dependences[i])
                logging.info("Land has deleted dependece: %s -> %s * %s", dependence_1, dependence_2, dependences[2])
                return
        logging.warning("Land has not deleted dependece: %s -> %s", dependence_1, dependence_2)

    # Con este método podemos cambiar el value en una dependencia
    def Change_Dependences_Value(self, dependence_1, dependence_2, new_value):
        for dependences in self.characteristic_dependences:
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                dependences[2] =  new_value
                logging.info("Land has changed dependece, new dependence: %s -> %s * %s", dependence_1, dependence_2, new_value)
                return
        logging.warning("Land has not changed dependece: %s -> %s * %s", dependence_1, dependence_2, new_value)

    def Add_Influences(self, influence_1, influence_2, value):
        for influences in self.characteristic_influences:      #Revisamos que no exista esta dependencia
            if influences[0] == influence_1 and influences[1] == influence_2:
                logging.warning("Land has not added influence: %s -> %s * %s", influence_1, influence_2, value)
                return 0    #Si existe devolvemos 0
        
        self.characteristic_influences.append([influence_1, influence_2, value]) #Agregamos la dependencia
        logging.info("Land has added influence: %s -> %s * %s", influence_1, influence_2, value)
        """  # Ejecutamos la influencia, en el resto de la simulación solo se aplicará para cambios en a
        a = self.distribitions["default"](self.characteristic[influence_2])
        b = self.characteristic[influence_2]
        self.characteristic[influence_2] = self.sum(b, self.mul(a, value))  """

    # Con este método podemos eliinar una dependencia
    def Delete_Influences(self, influence_1, influence_2):
        for i, influences in enumerate(self.characteristic_influences):
            if influences[0] == influence_1 and influences[1] == influence_2:
                del(self.characteristic_influences[i])                
                logging.info("Land has deleted influence: %s -> %s * %s", influence_1, influence_2, influences[2])
                return
        logging.warning("Land has not deleted influence: %s -> %s", influence_1, influence_2)

    # Con este método podemos cambiar el value en una dependencia
    def Change_Influences_Value(self, influence_1, influence_2, new_value):
        for influences in self.characteristic_influences:
            if influences[0] == influence_1 and influences[1] == influence_2:
                influences[2] =  new_value
                logging.info("Land has changed influence, new influence: %s -> %s * %s", influence_1, influence_2, new_value)
                return
        logging.warning("Land has not changed influence: %s -> %s * %s", influence_1, influence_2, new_value)


    #Método para añadir una interdependencia
    def Add_Inter_Dependence(self, entity_1, dependence_1, entity_2, dependence_2, value):
        if entity_1 == entity_2 or (entity_1 != '' and entity_1 not in self.societies.keys()) or (entity_2 != '' and entity_2 not in self.societies.keys()):
            logging.warning("interdependence has not added: Unrecognized entities")
            return
        for inter in self.inter_dependences:
            if (entity_1, dependence_1) in inter and (entity_2, dependence_2) in inter:
                logging.warning("interdependence has not added: Interdependence alredy exists")
                return
        self.inter_dependences.append([(entity_1, dependence_1), (entity_2, dependence_2), value])
        logging.info("interdependence was added")


    #Método para cambiar una interdependencia teniendo totalmente la dependencia a y b
    def Change_Inter_Dependence_Value(self, entity_1, dependence_1, entity_2, dependence_2, new_value):
        for inter, i in enumerate(self.inter_dependences):
            if (entity_1, dependence_1) in inter and (entity_2, dependence_2) in inter:
                self.inter_dependences[i][2] = new_value
                logging.info("Interdependence was changed")
                return
        logging.warning("Interdependence was not changed: interdependence does not exist")


    #Método para eliminar una interdependencia teniendo totalmente la dependencia a y b
    def Delete_Inter_Dependence(self, entity_1, dependence_1, entity_2, dependence_2):
        for inter, i in enumerate(self.inter_dependences):
            if (entity_1, dependence_1) in inter and (entity_2, dependence_2) in inter:
                del(self.inter_dependences[i])
                logging.info("Interdependence was deleted")
                return
        logging.warning("Interdependence was not deleted: interdependence does not exist")
                
    #Método para eliminar todas las interdependencias que incluyan a cierto a o b
    def Delete_All_Specific_Inter_Dependence(self, dependence, entity):
        for inter, i in enumerate(self.inter_dependences):
            if (entity, dependence) in inter:
                del(self.inter_dependences[i])
                logging.info("Interdependence was deleted")
                

    def sum(self,a, b):
        if isinstance(a,List):
            if isinstance(b,List):
                return [a[0] + b[0], a[1] + b[1]]
            return [a[0] + b, a[1] + b]
        return a + self.distribitions["default"](b)

    def mul(self,a, b):
        if isinstance(b,List):
            return [b[0] * a, b[1] * a]
        return a * b
    
    def comp(self, a, b):
        if isinstance(a,List) and isinstance(a,List):
            return a[0] > b[0] and a[1] < b[1] 
        return a * b
    
    def Move_Land_One_Day(self):
        actual_status = {}
        #Vamos por todas las dependencias
        for actual_dependence in self.characteristic_dependences:
            
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            a = self.distribitions["default"](self.Get_Characteristic_Value(actual_dependence[0]))            #Extraemos a
            b = self.Get_Characteristic_Value(actual_dependence[1])           #Extraemos b
            c = actual_dependence[2]  #Extraemos c

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
            actual_status[actual_dependence[1]] = self.operators["dependence"](a, b, c)
            logging.info("Land has update characteristic with dependece: %s -> %s * %s: %s = %s", actual_dependence[0], actual_dependence[1], actual_dependence[2], actual_dependence[1], self.characteristic[actual_dependence[1]])
        
        for actual_influence in self.characteristic_influences:
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            a = self.distribitions["default"](self.Get_Characteristic_Value(actual_influence[0]))            #Extraemos a
            b = self.Get_Characteristic_Value(actual_influence[1])           #Extraemos b
            c = actual_influence[2]  #Extraemos c
            act_a = actual_status.get(actual_influence[0])
            if act_a == None:
                act_a = a
            else:
                act_a = self.distribitions["default"](act_a)
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
            actual_status[actual_influence[1]] = self.operators["influence"](a, act_a, b, c)
            logging.info("Land has update characteristic with influence: %s -> %s * %s: %s = %s", actual_influence[0], actual_influence[1], actual_influence[2], actual_influence[1], self.characteristic[actual_influence[1]])
        
        for update in actual_status:
            self.Update_Characteristic_Value(update, actual_status[update])
        
        
    def Move_One_Day(self):
        
        for society in self.societies.values():
            society.Move_One_Day()
        
        actual_status={}
        for actual_inter in self.inter_dependences:
            a=0
            b=0
            c=0
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            if actual_inter[0][0] == '':
                a = self.distribitions["default"](self.Get_Characteristic_Value(actual_inter[0][1]))            #Extraemos a
            else:
                a = self.distribitions["default"](self.societies[actual_inter[0][0]].Get_Characteristic_Value(actual_inter[0][1]))            #Extraemos a
            if actual_inter[1][0] == '':
                b = self.Get_Characteristic_Value(actual_inter[1][1])           #Extraemos b
            else:
                b = self.societies[actual_inter[1][0]].Get_Characteristic_Value(actual_inter[1][1])           #Extraemos b
            c = actual_inter[2]  #Extraemos c

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
            actual_status[(actual_inter[1][0], actual_inter[1][1])] = self.operators["dependence"](a, b, c)
            logging.info("Land has update characteristic")
        
        for update in actual_status:
            if update[0] == '':
                self.Update_Characteristic_Value(update[1], actual_status[update])
            else:
                self.societies[update[0]].Update_Characteristic_Value(update[1], actual_status[update])
                
        self.Move_Land_One_Day()
        
        logging.info("Land has move one day")

    def Set_Default_Characteristics(self):
        self.Change_Characteristic("actual_resources", 1)       #Recursos actuales
        self.Change_Characteristic("resources_capacity", 1)      #Capacidad de recursos
        self.Change_Characteristic("temperature", [0,1])      #Temperatura
        self.Change_Characteristic("altitude", 1)             #Altitud
        self.Change_Characteristic("cozy_level", 1)             #Nivel de Acogimiento
        self.Change_Characteristic("fertility", [0,1])         #Fertilidad
        logging.info("Land has added default characteristic")

    def Set_Default_Dependences(self):
        pass
    