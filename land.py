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
        self.entities = {'': self} # Diccionario de entidades, primer elemento el terrenoasignado al caracter vacío, y luego las sociedades por el nombre de cada una
        self.operators = {
            "dependence": (lambda a, b, c : self.sum(b, self.mul(a, c))),
            "influence": (lambda old_a, act_a, b, c : self.sum(b, self.mul(self.sum(act_a, self.mul(old_a, -1)), c)))
            }
        self.distribitions = {
            "default": lambda c: random.randint(round(c[0]), round(c[1])) if isinstance(c, List) else c
        }
        
        logging.info("Land was created")

    #Añadir sociedad a la lista de entidades, crea una sociedad con el nombre y especie de entrada 
    def Add_Society(self, name, specie):
        if name == '':
            logging.warning("Society was not added")
            return
        for society in self.entities:
            if society == name:
                logging.warning("Society %s alredy exists", name)
                return False
        self.entities[name] = Society(name, specie)
        logging.info("Society %s was added", name)

    #Eliminar sociedad de nombre de la entrada
    def Delete_Society(self, name):
        if name not in self.entities.keys() or name == '':
            logging.warning("Society was not delete: Society do not exists")
            return 0
        #Ahora debemos eliminar toda interdependencia que incluya a esta especie
        for characteristic in self.entities[name].characteristic:
            self.Delete_All_Specific_Dependence(name, characteristic)
            self.Delete_All_Specific_Influence(name, characteristic)
        del(self.entities[name])
        logging.info("Society %s was deleted", name)

    #Tomar el valor de la caracteristica de entrada perteneciente a la sociedad de nombre: name
    #Si name = '' entonces se refiere a este terreno 
    def Get_Entities_Characteristic_value(self, name, characteristic):
        return self.entities[name].Get_Characteristic_Value(characteristic)
        
    #Cambiar el valor de la caracteristica de entrada perteneciente a la sociedad de nombre: name
    def Change_Entities_Characteristic(self, name, characteristic, value, lower = -math.inf, upper = math.inf):
        return self.entities[name].Change_Characteristic(characteristic, value, lower, upper)
    
    #Método para actualizar las características de la entidad de nombre name
    def Update_Entities_Characteristic(self, name, characteristic, value):
        return self.entities[name].Update_Characteristic_Value(characteristic, value)

    #Método para eliminar una característica de la entidad de nombre name
    def Delete_Entities_Characteristic(self, name, characteristic):
        return self.entities[name].Delete_Characteristic(characteristic)
     
    #Poner caracteristicas por defecto de la entidad de nombre name
    def Set_Default_Entities_Characteristic(self, name):
        return self.entities[name].Set_Default_Characteristics()

    #Tomar el valor de la caracteristica name de este terreno 
    def Get_Characteristic_Value(self, name):
        return self.characteristic[name][0]

    # Con este método podemos añadir o modificar el valor de la caracteristica name de este terreno
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

    # Con este método podemos eliminar el valor de la caracteristica name de este terreno
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("Land has deleted characteristic: %s", name)
            for i, dependence in enumerate(self.characteristic_dependences):
                if name in dependence:
                    del(dependence[i])
            return
        logging.warning("Land has not deleted characteristic: %s", name)

    # Con este método podemos actualizar el valor de la caracteristica name de este terreno
    # lower y upper de la caracteristica a actualizar
    def Update_Characteristic_Value(self, name, value):
        lower = self.characteristic[name][1]
        upper = self.characteristic[name][2]
        self.Change_Characteristic(name, value, lower, upper) 
   
    # Con este método podemos agregar una dependencia de la forma a -> b * c
    # Donde a es (dependence_1, entity_1), b es (dependence_2, entity_2) y c es value
    def Add_Dependence(self, entity_1, dependence_1, entity_2, dependence_2, value):
        if entity_1 not in self.entities.keys() or entity_2 not in self.entities.keys():
            logging.warning("dependence was not added: Unrecognized entities")
            return
        for dependence in self.characteristic_dependences:
            if (entity_1, dependence_1) == dependence[0] and (entity_2, dependence_2) == dependence[1]:
                logging.warning("dependence was not added: dependence alredy exists")
                return
        self.characteristic_dependences.append([(entity_1, dependence_1), (entity_2, dependence_2), value])
        logging.info("dependence was added")

    #Método para cambiar una dependencia teniendo totalmente la dependencia a y b
    def Change_Dependences_Value(self, entity_1, dependence_1, entity_2, dependence_2, new_value):
        if entity_1 not in self.entities.keys() and entity_2 not in self.entities.keys():
            logging.warning("dependence was not added: Unrecognized entities")
            return
        for i, dependence in enumerate(self.characteristic_dependences):
            if (entity_1, dependence_1) == dependence[0] and (entity_2, dependence_2) == dependence[1]:
                self.characteristic_dependences[i][2] = new_value
                logging.info("dependence was changed")
                return
        logging.warning("dependence was not changed: dependence does not exist")

    #Método para eliminar una dependencia teniendo totalmente la dependencia a y b
    def Delete_Dependence(self, entity_1, dependence_1, entity_2, dependence_2):
        for i, dependence in enumerate(self.characteristic_dependences):
            if (entity_1, dependence_1) == dependence[0] and (entity_2, dependence_2) == dependence[1]:
                del(self.characteristic_dependences[i])
                logging.info("dependence was deleted")
                return
        logging.warning("dependence was not deleted: dependence does not exist")
                
    #Método para eliminar todas las dependencias que incluyan la caracteristica characteristic de la entidad name
    def Delete_All_Specific_Dependence(self, entity, characteristic):
        for i, dependence in enumerate(self.characteristic_dependences):
            if (entity, characteristic) in dependence:
                del(self.characteristic_dependences[i])
                logging.info("dependence was deleted")
                
    # Con este método podemos cambiar el value en una influencia
    def Add_Influences(self, entity_1, influence_1, entity_2, influence_2, value):
        for influences in self.characteristic_influences:      #Revisamos que no exista esta dependencia
            if influences[0] == (entity_1, influence_1) and influences[1] == (entity_2, influence_2):
                logging.warning("Land has not added influence: %s -> %s * %s", influence_1, influence_2, value)
                return 0    #Si existe devolvemos 0
        
        self.characteristic_influences.append([(entity_1, influence_1), (entity_2, influence_2), value]) #Agregamos la dependencia
        logging.info("Land has added influence: %s -> %s * %s", influence_1, influence_2, value)
        

    # Con este método podemos cambiar el value en una influencia
    def Change_Influences_Value(self, entity_1, influence_1, entity_2, influence_2, new_value):
        for influences in self.characteristic_influences:
            if influences[0] == (entity_1, influence_1) and influences[1] == (entity_2, influence_2):
                influences[2] =  new_value
                logging.info("Land has changed influence, new influence: %s -> %s * %s", influence_1, influence_2, new_value)
                return
        logging.warning("Land has not changed influence: %s -> %s * %s", influence_1, influence_2, new_value)
    
    # Con este método podemos eliinar una influencia
    def Delete_Influences(self, entity_1, influence_1, entity_2, influence_2):
        for i, influences in enumerate(self.characteristic_influences):
            if influences[0] == (entity_1, influence_1) and influences[1] == (entity_2, influence_2):
                del(self.characteristic_influences[i])                
                logging.info("Land has deleted influence: %s -> %s * %s", influence_1, influence_2, influences[2])
                return
        logging.warning("Land has not deleted influence: %s -> %s", influence_1, influence_2)

    #Método para eliminar todas las influencias que incluyan la caracteristica characteristic de la entidad name
    def Delete_All_Specific_Influence(self, entity, characteristic):
        for i, influence in enumerate(self.characteristic_influences):
            if (entity, characteristic) in influence:
                del(self.characteristic_influences[i])
                logging.info("dependence was deleted")

    #nuestras operaciones para operar con rangos o valores numericos 
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
    
    #Avanzar un dia en el terreno, modifica las caracteristicas del terreno y sus sociedades con las dependencias e influencias previamente establecidas
    def Move_One_Day(self):   
        #Se guarda un diccionario de modificaciones de las dependencias     
        actual_status={}
        for actual_dependence in self.characteristic_dependences:
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            a = self.distribitions["default"](self.entities[actual_dependence[0][0]].Get_Characteristic_Value(actual_dependence[0][1]))  #Extraemos a
            b = self.entities[actual_dependence[1][0]].Get_Characteristic_Value(actual_dependence[1][1])           #Extraemos b
            c = actual_dependence[2]  #Extraemos c

            #se hace una separación por casos:
            #Si a tiene dos coordenadas, entonces el valor de a es directamente un random de ese intervalo
            #Si a es un valor, entonces a es directamente igual a ese valor
            #Ya sea que b tiene un valor, o dos coordenadas, estos no se verifican mediante un random, sino que
            #se multiplican a partir de los casos de c:

            #Si b es un valor y c una coordenada, entonces a se multiplica por un random proporcionado por el intervalo de c
            #Si b es un valor y c un valor, se multiplican
            #Si b es una coordenada (b1, b2), y c una coordenada (c1, c2), entonces se debe hacer:
            # (b1, b2) = (b1, b2) + (c1*a, c2*a)
            #Si b es una coordenada y c un valor entonces se multiplica ambas a por c
            actual_status[(actual_dependence[1][0], actual_dependence[1][1])] = self.operators["dependence"](a, b, c)
            logging.info("Land has update characteristic")
        
        #Se guarda el diccionario final resultado de aplicar las dependencias y luego las influenncias que traen las mismas
        final_status= actual_status.copy()
        for actual_influence in self.characteristic_influences:
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            a = self.distribitions["default"](self.entities[actual_influence[0][0]].Get_Characteristic_Value(actual_influence[0][1]))  #Extraemos a
            b = self.entities[actual_influence[1][0]].Get_Characteristic_Value(actual_influence[1][1])           #Extraemos b
            c = actual_influence[2]  #Extraemos c
            act_a = actual_status.get(actual_influence[0])
            if act_a == None:
                act_a = a
            else:
                act_a = self.distribitions["default"](act_a)
            
            #Opera parecido a las dependencias pero no nos interesa modificar atendiendo al valor sino a los cambios surgidos mientras avanza el día
            
            final_status[(actual_influence[1][0], actual_influence[1][1])] = self.operators["influence"](a, act_a, b, c)
            logging.info("Land has update characteristic with influence: %s -> %s * %s", actual_influence[0], actual_influence[1], actual_influence[2])
        
        #Los cambios finales resultantes de las dependencias e influencias actualizan las caracteristicas modificadas
        for update in final_status:
            self.entities[update[0]].Update_Characteristic_Value(update[1], final_status[update])        
        logging.info("Land has move one day")

    def Set_Default_Characteristics(self):
        self.Change_Characteristic("actual_resources", 1, 0)       #Recursos actuales
        self.Change_Characteristic("resources_capacity", 1, 0)      #Capacidad de recursos
        self.Change_Characteristic("temperature", [0,1])      #Temperatura
        self.Change_Characteristic("altitude", 1)             #Altitud
        self.Change_Characteristic("cozy_level", 1, 0)             #Nivel de Acogimiento
        self.Change_Characteristic("fertility", [0,1])         #Fertilidad
        logging.info("Land has added default characteristic")

    def Set_Default_Dependences(self):
        pass
    