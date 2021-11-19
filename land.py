import random
from typing import List, Tuple
import logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

class Land:

    def __init__(self):

        self.characteristic = {}
        self.characteristic_dependences = [] # dependence_1 -> dependence_2 * value
        
        logging.info("Land was created")



    # Con este método podemos añadir o modificar una característica y su valor
    def Change_Characteristic(self, name, value):
        self.characteristic[name] = value
        logging.info("Land has added/changed characteristic: %s with value:%s", name, value)

    # Con este método podemos eliminar una característica y su valor
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("Land has deleted characteristic: %s", name)
            return
        logging.warning("Land has not deleted characteristic: %s", name)

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
                dependences[2] = new_value
                logging.info("Land has changed dependece, new dependence: %s -> %s * %s", dependence_1, dependence_2, new_value)
                return
        logging.warning("Land has not changed dependece: %s -> %s * %s", dependence_1, dependence_2, new_value)


    def Move_One_Day(self):
        
        #Vamos por todas las dependencias
        for actual_dependence in self.characteristic_dependences:
            
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            a = self.characteristic[actual_dependence[0]]            #Extraemos a
            b = self.characteristic[actual_dependence[1]]            #Extraemos b
            c = actual_dependence[2]                                 #Extraemos c

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
                a = random.randint(round(a[0]), round(a[1]))

            if(isinstance(b, List)):
                if(isinstance(c, List)):
                    self.characteristic[actual_dependence[1]] = [b[0] + c[0]*a, b[1] + c[1]*a]
                else:
                    self.characteristic[actual_dependence[1]] = [b[0] + c*a, b[1] + c*a]
            else:
                if(isinstance(c, List)):
                    self.characteristic[actual_dependence[1]] = b + a * random.randint(round(c[0]), round(c[1]))
                else:
                    self.characteristic[actual_dependence[1]] = b + a * c
            logging.info("Land has update characteristic with dependece: %s -> %s * %s: %s = %s", actual_dependence[0], actual_dependence[1], actual_dependence[2], actual_dependence[1], self.characteristic[actual_dependence[1]])
        logging.info("Land has move one day")


    def Set_Default_Characteristics(self):
        self.characteristic["actual_resources"] = 1       #Recursos actuales
        self.characteristic["resources_capacity"] = 1     #Capacidad de recursos
        self.characteristic["temperature"] = [0, 1]       #Temperatura
        self.characteristic["altitude"] = 1               #Altitud
        self.characteristic["cozy_level"] = 1             #Nivel de Acogimiento
        self.characteristic["fertility"] = [0, 1]         #Fertilidad
        logging.info("Land has added default characteristic")

    def Set_Default_Dependences(self):
        pass
