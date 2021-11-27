import random
from typing import List, Tuple
import logging
import math


class Society:

    def __init__(self, name):

        self.name = name

        self.characteristic = {}
        self.characteristic_dependences = [] # dependence_1 -> dependence_2 * value
        self.characteristic_influences = [] # influence_1 -> influence_2 * value
        #self.characteristic_limits = [] # limit_1 -> limit_2 * value
        self.operators = {
            "dependence": (lambda a, b, c : self.sum(b, self.mul(a, c))),
            "influence": (lambda old_a, act_a, b, c : self.sum(b, self.mul(self.sum(act_a, self.mul(old_a, -1)), c))),
            #"limit": (lambda a, b, c : b if b < self.mul(a, c) else self.mul(a, c)),
            }
        self.distribitions = {
            "default": lambda c: random.randint(round(c[0]), round(c[1])) if isinstance(c, List) else c
        }
        
        logging.info("Society was created")

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
        logging.info("Society has added/changed characteristic: %s with value:%s", name, value)

    # Con este método podemos eliminar una característica y su valor
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("Society has deleted characteristic: %s", name)
            for i, dependence in enumerate(self.characteristic_dependences):
                if name in dependence:
                    del(dependence[i])
            return
        logging.warning("Society has not deleted characteristic: %s", name)

    def Update_Characteristic_Value(self, name, value):
        lower = self.characteristic[name][1]
        upper = self.characteristic[name][2]
        self.Change_Characteristic(name, value, lower, upper) 
    
    # Con este método podemos agregar una dependencia de la forma a -> b * c
    # Donde a es dependence_1, b es dependence_2 y c es value
    def Add_Dependences(self, dependence_1, dependence_2, value):
        for dependences in self.characteristic_dependences:      #Revisamos que no exista esta dependencia
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                logging.warning("Society has not added dependece: %s -> %s * %s", dependence_1, dependence_2, value)
                return 0    #Si existe devolvemos 0
        self.characteristic_dependences.append([dependence_1, dependence_2, value]) #Agregamos la dependencia
        logging.info("Society has added dependece: %s -> %s * %s", dependence_1, dependence_2, value)

    # Con este método podemos eliinar una dependencia
    def Delete_Dependences(self, dependence_1, dependence_2):
        for i, dependences in enumerate(self.characteristic_dependences):
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                del(self.characteristic_dependences[i])
                logging.info("Society has deleted dependece: %s -> %s * %s", dependence_1, dependence_2, dependences[2])
                return
        logging.warning("Society has not deleted dependece: %s -> %s", dependence_1, dependence_2)

    # Con este método podemos cambiar el value en una dependencia
    def Change_Dependences_Value(self, dependence_1, dependence_2, new_value):
        for dependences in self.characteristic_dependences:
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                dependences[2] =  new_value
                logging.info("Society has changed dependece, new dependence: %s -> %s * %s", dependence_1, dependence_2, new_value)
                return
        logging.warning("Society has not changed dependece: %s -> %s * %s", dependence_1, dependence_2, new_value)

    def Add_Influences(self, influence_1, influence_2, value):
        for influences in self.characteristic_influences:      #Revisamos que no exista esta dependencia
            if influences[0] == influence_1 and influences[1] == influence_2:
                logging.warning("Society has not added influence: %s -> %s * %s", influence_1, influence_2, value)
                return 0    #Si existe devolvemos 0
        
        self.characteristic_influences.append([influence_1, influence_2, value]) #Agregamos la dependencia
        logging.info("Society has added influence: %s -> %s * %s", influence_1, influence_2, value)
        """  # Ejecutamos la influencia, en el resto de la simulación solo se aplicará para cambios en a
        a = self.distribitions["default"](self.characteristic[influence_2])
        b = self.characteristic[influence_2]
        self.characteristic[influence_2] = self.sum(b, self.mul(a, value))  """

    # Con este método podemos eliinar una dependencia
    def Delete_Influences(self, influence_1, influence_2):
        for i, influences in enumerate(self.characteristic_influences):
            if influences[0] == influence_1 and influences[1] == influence_2:
                del(self.characteristic_influences[i])                
                logging.info("Society has deleted influence: %s -> %s * %s", influence_1, influence_2, influences[2])
                return
        logging.warning("Society has not deleted influence: %s -> %s", influence_1, influence_2)

    # Con este método podemos cambiar el value en una dependencia
    def Change_Influences_Value(self, influence_1, influence_2, new_value):
        for influences in self.characteristic_influences:
            if influences[0] == influence_1 and influences[1] == influence_2:
                influences[2] =  new_value
                logging.info("Society has changed influence, new influence: %s -> %s * %s", influence_1, influence_2, new_value)
                return
        logging.warning("Society has not changed influence: %s -> %s * %s", influence_1, influence_2, new_value)

    """ 
    def Add_Limit(self, limit_1, limit_2, value):
        for limits in self.characteristic_limits:      #Revisamos que no exista esta dependencia
            if limits[0] == limit_1 and limits[1] == limit_2:
                logging.warning("Society has not added limit: %s -> %s * %s", limit_1, limit_2, value)
                return 0    #Si existe devolvemos 0        
        self.characteristic_limits.append([limit_1, limit_2, value]) #Agregamos la dependencia
        logging.info("Society has added limit: %s -> %s * %s", limit_1, limit_2, value)

    # Con este método podemos eliinar una dependencia
    def Delete_Limit(self, limit_1, limit_2):
        for i, limits in enumerate(self.characteristic_limits):
            if limits[0] == limit_1 and limits[1] == limit_2:
                del(self.characteristic_limits[i])
                logging.info("Society has deleted limit: %s -> %s * %s", limit_1, limit_2, limits[2])
                return
        logging.warning("Society has not deleted limit: %s -> %s", limit_1, limit_2)

    # Con este método podemos cambiar el value en una dependencia
    def Change_Limits_Value(self, limit_1, limit_2, new_value):
        for limits in self.characteristic_limits:
            if limits[0] == limit_1 and limits[1] == limit_2:
                limits[2] =  new_value
                logging.info("Society has changed dependece, new limit: %s -> %s * %s", limit_1, limit_2, new_value)
                return
        logging.warning("Society has not changed limit: %s -> %s * %s", limit_1, limit_2, new_value)

    """
    def Move_One_Day(self):
        
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
            logging.info("Society has update characteristic with dependece: %s -> %s * %s: %s = %s", actual_dependence[0], actual_dependence[1], actual_dependence[2], actual_dependence[1], self.characteristic[actual_dependence[1]])
        
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
            logging.info("Society has update characteristic with influence: %s -> %s * %s: %s = %s", actual_influence[0], actual_influence[1], actual_influence[2], actual_influence[1], self.characteristic[actual_influence[1]])
        
        for update in actual_status:
            self.Update_Characteristic_Value(update, actual_status[update])
        logging.info("Society has move one day")


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
        logging.info("Society has added default characteristic")

    def Set_Default_Dependences(self):
        pass
