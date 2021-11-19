
import random
from typing import List, Tuple
import logging

class Species:

    def __init__(self, name):
        logging.basicConfig(filename='Logs/specie_log.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

        self.name = name

        self.characteristic = {}

        self.characteristic["population"] = 1              #Población

        self.characteristic_dependences = []  # dependence_1 -> dependence_2 * value, lo que se traduce como:
                                              # dependence_2 += dependence_1 * value
        logging.info("Specie %s was created", name)



    # Con este método podemos añadir o modificar una característica y su valor
    def Change_Characteristic(self, name, value):
        self.characteristic[name] = value
        logging.info("%s has added/changed characteristic: %s with value:%s", self.name, name, value)
        

    # Con este método podemos eliminar una característica y su valor
    def Delete_Characteristic(self, name):
        if name in self.characteristic:
            del(self.characteristic[name])
            logging.info("%s has deleted characteristic: %s", self.name, name)
            return
        logging.warning("%s has not deleted characteristic: %s", self.name, name)

    # Con este método podemos agregar una dependencia de la forma a -> b * c
    # Donde a es dependence_1, b es dependence_2 y c es value
    def Add_Dependences(self, dependence_1, dependence_2, value):
        for dependences in self.characteristic_dependences:      #Revisamos que no exista esta dependencia
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                logging.warning("%s has not added dependece: %s -> %s * %s", self.name, dependence_1, dependence_2, value)
                return 0    #Si existe devolvemos 0
        self.characteristic_dependences.append([dependence_1, dependence_2, value]) #Agregamos la dependencia
        logging.info("%s has added dependece: %s -> %s * %s", self.name, dependence_1, dependence_2, value)
        

    # Con este método podemos eliminar una dependencia
    def Delete_Dependences(self, dependence_1, dependence_2):
        for i, dependences in enumerate(self.characteristic_dependences):
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                del(self.characteristic_dependences[i])
                logging.info("%s has deleted dependece: %s -> %s * %s", self.name, dependence_1, dependence_2, dependences[2])
                return
        logging.warning("%s has not deleted dependece: %s -> %s", self.name, dependence_1, dependence_2)

    # Con este método podemos cambiar el value en una dependencia
    def Change_Dependences_Value(self, dependence_1, dependence_2, new_value):
        for dependences in self.characteristic_dependences:
            if dependences[0] == dependence_1 and dependences[1] == dependence_2:
                dependences[2] = new_value
                logging.info("%s has changed dependece, new dependence: %s -> %s * %s", self.name, dependence_1, dependence_2, new_value)
                return
        logging.warning("%s has not changed dependece: %s -> %s * %s", self.name, dependence_1, dependence_2, new_value)


    def Move_One_Day(self):
        
        #Vamos por todas las dependencias
        for actual_dependence in self.characteristic_dependences:
            
            #Las dependencias se guardan de la forma a -> b * c, que se traduce como b += a * c
            #Guardamos la dependencia actual
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
            logging.info("%s has update characteristic with dependece: %s -> %s * %s", self.name, actual_dependence[0], actual_dependence[1], actual_dependence[2])
            

    def Set_Default_Characteristics(self):
        self.characteristic["death_rate"] = [0, 1]         #Mortalidad
        self.characteristic["birth_rate"] = [0, 1]         #Natalidad
        self.characteristic["life_expectation"] = 1        #Esperanza de vida
        self.characteristic["gestation"] = 1               #Período de Gestación
        self.characteristic["reproduction_number"] = [0,1] #Número de reproducción
        self.characteristic["size"] = 1                    #Tamaño
        self.characteristic["intellect"] = 1               #Intelecto
        self.characteristic["strength"] = 1                #Fuerza
        self.characteristic["evolution_rate"] = 1          #Capacidad de evolución
        self.characteristic["actual_growth"] = 1           #Crecimiento Actual
        self.characteristic["economy"] = 1                 #Economía
        self.characteristic["foreign_tolerance"] = 1       #Tolerancia a extranjeros
        logging.info("%s has added default characteristic", self.name)

    def Set_Default_Dependences(self):
        pass
