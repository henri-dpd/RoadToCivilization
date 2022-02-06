import random
from typing import List, Tuple
import logging
import math

from Simulation.characteristic import Characteristic
from Simulation.dependence import Dependence
from Simulation.society import Society
import Simulation.operators as operators

class Land:

    #Definido un diccionario caracteristicas {"caracteristica":[<valor>,<limInf>,<limSup>]} 
    #Definido una lista dependencias [<entidad1>,<caracteristicaA>,<entidad2>,<caracteristicaB>,<valor>] 
    #Definido una lista influencias [<entidad1>,<caracteristicaA>,<entidad2>,<caracteristicaB>,<valor>] 
    #Definido un diccionario entidades {"entidad": entidad} incluido land asignando '' como su llave 
    #Definido un diccionario operadores {"operador": funcion} para calcular dependencias, influencias u otro proceso que describa el usuario 
    #Definido un diccionario distribuciones {"distribucion": funcion} para calcular un valor en un rango de acuerdo a la distribucion establecida
    def __init__(self, pos):
        self.pos = pos
        self.characteristic = {}
        self.characteristic_dependences = [] # dependence_1 -> dependence_2 * value
        self.characteristic_influences = [] # influence_1 -> influence_2 * value
        self.entities = {'': self} # Diccionario de entidades, primer elemento el terrenoasignado al caracter vacío, y luego las sociedades por el nombre de cada una
        
        
        logging.info("Land was created")

    def Copy(self):
        copy_land = Land(self.pos)
        for characteristics_name in self.characteristic:
            copy_land.characteristic[characteristics_name] = self.characteristic[characteristics_name].Copy()
        for dependence in self.characteristic_dependences:
            copy_land.characteristic_dependences.append(dependence)
        for influence in self.characteristic_influences:
            copy_land.characteristic_influences.append(influence)
        for entity_name in self.entities:
            if entity_name != '':
                copy_land.entities[entity_name] = self.entities[entity_name].Copy()
        return copy_land

    #Añadir sociedad a la lista de entidades, crea una sociedad con el nombre y especie de entrada 
    def Add_Society(self, name, species):
        if name == '':
            logging.warning("Society was not added")
            return
        for society in self.entities:
            if society == name:
                logging.warning("Society %s alredy exists", name)
                return False
        self.entities[name] = Society(name, species, self.pos)
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
            
        self.entities[name].Delete()
        del(self.entities[name])
        logging.info("Society %s was deleted", name)

    #Tomar el valor de la caracteristica de entrada perteneciente a la sociedad de nombre: name
    #Si name = '' entonces se refiere a este terreno 
    def Get_Entities_Characteristic_value(self, name, characteristic):
        if not name in self.entities:
            raise Exception("La sociedad " + name + " no existe")
        return self.entities[name].Get_Characteristic_Value(characteristic)
        
    #Cambiar el valor de la caracteristica de entrada perteneciente a la sociedad de nombre: name
    def Change_Entities_Characteristic(self, name, characteristic, value, lower = -math.inf, upper = math.inf, mutablility = -1, distr_function = None):
        return self.entities[name].Change_Characteristic(characteristic, value, lower, upper, mutablility, distr_function)
    
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
        if name in self.characteristic:
            return self.characteristic[name].value

    def z_getCharacteristic(self, name):
        return self.Get_Characteristic_Value(name)

    # Con este método podemos añadir o modificar el valor de la caracteristica name de este terreno
    def Change_Characteristic(self, name, value, lower = -math.inf, upper = math.inf, mutability = 1, distr_function = None):
        if name in self.characteristic:
            self.characteristic[name].Change_Characteristic(name, value, lower, upper, mutability, distr_function)
        else:
            self.characteristic[name] = Characteristic(name, value, lower, upper, mutability, distr_function)

    def z_changeCharacteristic(self, name, value, lower, upper, mutability, distr_function):
        self.Change_Characteristic(name, value, lower, upper, mutability, distr_function)

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
        raise Exception("Land already has not the characteristic: " + name)

    def z_deleteCharacteristic(self, name):
        self.Delete_Characteristic(self, name)

    # Con este método podemos actualizar el valor de la caracteristica name de este terreno
    # lower y upper de la caracteristica a actualizar
    def Update_Characteristic_Value(self, name, value):
        if name in self.characteristic:
            self.characteristic[name].Update_Characteristic_Value(value)
   
    # Con este método podemos agregar una dependencia de la forma a -> b * c
    # Donde a es (dependence_1, entity_1), b es (dependence_2, entity_2) y c es value
    def Add_Dependence(self, entity_1, dependence_1, entity_2, dependence_2, value, sum = None, mul = None):
        if entity_1 not in self.entities.keys() or entity_2 not in self.entities.keys():
            logging.warning("Dependence was not added: Unrecognized entities")
            return False
        dep = Dependence(self.pos, entity_1, dependence_1, self.pos, entity_2, dependence_2, value, sum, mul)
        for dependence in self.characteristic_dependences:
            if dependence.IsInstance(dep):
                logging.warning("Dependence was not added: dependence alredy exists")
                return False
        self.characteristic_dependences.append(dep)
        logging.info("Dependence was added")
        return True

    def z_addDependence(self, entity_1, dependence_1, entity_2, dependence_2, value, sum, mul):
        return self.Add_Dependence(entity_1, dependence_1, entity_2, dependence_2, value, sum, mul)

    #Método para cambiar una dependencia teniendo totalmente la dependencia a y b
    def Change_Dependences_Value(self, entity_1, dependence_1, entity_2, dependence_2, new_value):
        if entity_1 not in self.entities.keys() and entity_2 not in self.entities.keys():
            logging.warning("Dependence was not added: Unrecognized entities")
            return
        dep = Dependence(self.pos, entity_1, dependence_1, self.pos, entity_2, dependence_2, new_value)
        for i, dependence in enumerate(self.characteristic_dependences):
            if dependence.IsInstance(dep):
                self.characteristic_dependences[i].Change_C(new_value)
                logging.info("Dependence was changed")
                return
        logging.warning("Dependence was not changed: dependence does not exist")

    #Método para eliminar una dependencia teniendo totalmente la dependencia a y b
    def Delete_Dependence(self, entity_1, dependence_1, entity_2, dependence_2):
        dep = Dependence(self.pos, entity_1, dependence_1, self.pos, entity_2, dependence_2, 0)
        for i, dependence in enumerate(self.characteristic_dependences):
            if dependence.IsInstance(dep):
                del(self.characteristic_dependences[i])
                logging.info("Dependence was deleted")
                return True
        logging.warning("Dependence was not deleted: dependence does not exist")
        return False
    
    def z_deleteDependence(self, entity_1, dependence_1, entity_2, dependence_2):
        return self.Delete_Dependence(entity_1, dependence_1, entity_2, dependence_2)
                
    #Método para eliminar todas las dependencias que incluyan la caracteristica characteristic de la entidad name
    def Delete_All_Specific_Dependence(self, entity, characteristic):
        for i, dependence in enumerate(self.characteristic_dependences):
            if dependence.Is_In((self.pos, entity, characteristic)):
                del(self.characteristic_dependences[i])
                logging.info("Dependence was deleted")
                
    # Con este método podemos cambiar el value en una influencia
    def Add_Influences(self, entity_1, influence_1, entity_2, influence_2, value, sum = None, mul = None):
        if entity_1 not in self.entities.keys() and entity_2 not in self.entities.keys():
            logging.warning("Influence was not added: Unrecognized entities")
            return False
        infl = Dependence(self.pos, entity_1, influence_1, self.pos, entity_2, influence_2, value, sum, mul)
        for influences in self.characteristic_influences:      #Revisamos que no exista esta dependencia
            if influences.IsInstance(infl):
                logging.warning("Land has added influence: Influence alredy exists")
                return False    #Si existe devolvemos 0
        self.characteristic_influences.append(infl) #Agregamos la dependencia
        logging.info("Land has added influence: %s -> %s * %s", influence_1, influence_2, value)
        return True

    def z_addInfluence(self, entity_1, influence_1, entity_2, influence_2, value, sum, mul):
        return self.Add_Dependence(entity_1, influence_1, entity_2, influence_2, value, sum, mul)
        
    # Con este método podemos cambiar el value en una influencia
    def Change_Influences_Value(self, entity_1, influence_1, entity_2, influence_2, new_value):
        if entity_1 not in self.entities.keys() and entity_2 not in self.entities.keys():
            logging.warning("Influence was not added: Unrecognized entities")
            return
        infl = Dependence(self.pos, entity_1, influence_1, self.pos, entity_2, influence_2, new_value)
        for i,influences in enumerate(self.characteristic_influences):
            if influences.IsInstance(infl):
                self.characteristic_influences[i].Change_C(new_value)
                logging.info("Land has changed influence, new influence")
                return
        logging.warning("Land has not changed influence")
    
    # Con este método podemos eliinar una influencia
    def Delete_Influences(self, entity_1, influence_1, entity_2, influence_2):
        infl = Dependence(self.pos, entity_1, influence_1, self.pos, entity_2, influence_2, 0)
        for i, influences in enumerate(self.characteristic_influences):
            if influences.IsInstance(infl):
                del(self.characteristic_influences[i])                
                logging.info("Land has deleted influence")
                return True
        logging.warning("Land has not deleted influence")
        return False

    def z_deleteInfluence(self, entity_1, influence_1, entity_2, influence_2):
        return self.Delete_Influences(entity_1, influence_1, entity_2, influence_2)
    
    #Método para eliminar todas las influencias que incluyan la caracteristica characteristic de la entidad name
    def Delete_All_Specific_Influence(self, entity, characteristic):
        for i, influence in enumerate(self.characteristic_influences):
            if influence.Is_In((self.pos, entity, characteristic)):
                del(self.characteristic_influences[i])
                logging.info("dependence was deleted")

    #Avanzar un dia en el terreno, modifica las caracteristicas del terreno y sus sociedades con las dependencias e influencias previamente establecidas
    def Move_One_Day(self):
        #Se guarda un diccionario de modificaciones de las dependencias     
        actual_status={}
        for actual_dependence in self.characteristic_dependences:
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            distribution = self.entities[actual_dependence.entity_1].characteristic[actual_dependence.characteristic_1].distr_function
            a = distribution(self.entities[actual_dependence.entity_1].Get_Characteristic_Value(actual_dependence.characteristic_1))  #Extraemos a
            b = self.entities[actual_dependence.entity_2].Get_Characteristic_Value(actual_dependence.characteristic_2)           #Extraemos b
            c = actual_dependence.c  #Extraemos c
            
            plus  = actual_dependence.plus_function
            mult  = actual_dependence.mult_function

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
            
            result = operators.dependence(plus, mult)(a, b, c)
            actual_status[(actual_dependence.entity_2, actual_dependence.characteristic_2)] = result

            change_value = 0
            
            if isinstance(result, List):
                change_value = (result[0] - b[0] + result[1] - b[1])/2
            else:
                change_value = result - b
 
            self.Learning_for_Evolution(actual_dependence, a, change_value)

            logging.info("Land has update characteristic")
        
        #Se guarda el diccionario final resultado de aplicar las dependencias y luego las influenncias que traen las mismas
        final_status= actual_status.copy()
        for actual_influence in self.characteristic_influences:
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            distribution = self.entities[actual_influence.entity_1].characteristic[actual_influence.characteristic_1].distr_function
            a = distribution(self.entities[actual_influence.entity_1].Get_Characteristic_Value(actual_influence.characteristic_1))  #Extraemos a
            b = self.entities[actual_influence.entity_2].Get_Characteristic_Value(actual_influence.characteristic_2)           #Extraemos b
            c = actual_influence.c  #Extraemos c
            act_a = actual_status.get((actual_influence.entity_1, actual_influence.characteristic_1))
            if act_a == None:
                act_a = a
            else:
                act_a = distribution(act_a)
            
            plus  = actual_influence.plus_function
            mult  = actual_influence.mult_function

            #Opera parecido a las dependencias pero no nos interesa modificar atendiendo al valor sino a los cambios surgidos mientras avanza el día
            
            final_status[(actual_influence.entity_2, actual_influence.characteristic_2)] = operators.influence(plus, mult)(a, act_a, b, c)
            logging.info("Land has update characteristic with influence: %s -> %s * %s", actual_influence.characteristic_1, actual_influence.characteristic_2, actual_influence.c)
        
        #Los cambios finales resultantes de las dependencias e influencias actualizan las caracteristicas modificadas
        for update in final_status:
            self.entities[update[0]].Update_Characteristic_Value(update[1], final_status[update])        
        logging.info("Land has move one day")

    #Permite habilitar la clase Evolución para alguna de las sociedades Sociedad
    def Start_Evolution(self, society_name):
        for society in self.entities:
            if society_name == society:
                society.Start_Evolution()

    def Learning_for_Evolution(self, in_inter_dependence, value, change_value):
        entity = in_inter_dependence.entity_2
        if entity != '' and self.entities[entity].enable_evolution:
            self.entities[in_inter_dependence.entity_2].Learning_for_Evolution(in_inter_dependence, value, change_value)

    def Request_for_Evolution(self):
        dependences_request = []

        for entity in self.entities:
            if entity != '' and self.entities[entity].enable_evolution:
                request = self.entities[entity].Request_for_Evolution()
                if request != None:
                    actual_dependence = request[1]
                    if actual_dependence.pos_2 == self.pos:
                        self.Request_From_Society(request[0], actual_dependence)
                    else:
                        dependences_request.append(request)

        return dependences_request

    def Request_From_Society(self, value, inter_dependence):
        entity_2 = inter_dependence.entity_2
        characteristic_2 = inter_dependence.characteristic_2

        if value == 1:
            mutability = self.entities[entity_2].characteristic[characteristic_2].mutability
            if operators.distribution_default([0, 10]) > mutability:
                modify_value = operators.distribution_default([5, 20])
                node_value = self.Get_Entities_Characteristic_value(inter_dependence.entity_2, inter_dependence.characteristic_2) * modify_value / 100
                self.entities[inter_dependence.entity_1].Request_from_Land(value, inter_dependence, node_value)
                self.Add_Dependence(inter_dependence.entity_1, inter_dependence.characteristic_1,
                                    inter_dependence.entity_2, inter_dependence.characteristic_2,
                                    inter_dependence.c)
        if value == 0:
            self.Change_Dependences_Value(inter_dependence.entity_1, inter_dependence.characteristic_1,
                                          inter_dependence.entity_2, inter_dependence.characteristic_2,
                                          inter_dependence.c)
        if value == -1:
            self.Delete_Dependence(inter_dependence.entity_1, inter_dependence.characteristic_1,
                                   inter_dependence.entity_2, inter_dependence.characteristic_2)
            self.entities[inter_dependence.entity_1].Request_from_Land(value, inter_dependence)
        
    def Request_From_Simulation(self, value, inter_dependence, node_value):
        self.entities[inter_dependence.entity_1].Request_from_Land(value, inter_dependence, node_value)

    def Set_Default_Characteristics(self):
        self.Change_Characteristic("Recursos Actuales", 1, 0)
        self.Change_Characteristic("Capacidad de Recursos", 1, 0)
        self.Change_Characteristic("Temperatura", [0,1])
        self.Change_Characteristic("Altitud", 1)
        self.Change_Characteristic("Nivel de Acogimiento", 1, 0)
        self.Change_Characteristic("Fertilidad", [0,1])
        logging.info("Land has added default characteristic")

    def Set_Default_Dependences(self):
        pass
    