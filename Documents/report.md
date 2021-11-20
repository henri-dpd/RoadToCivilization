# Road To Civilization
Proyecto asignaturas de **Simulación**, **Inteligencia Artificial** y **Compilación** del 3er año de Ciencias de la Computación de la Universidad de la Habana.

Desarrolladores:
* Alejandro Escobar Giraudy (C312)
* Airelys Collazo Pérez (C312)
* Henri Daniel Peña Dequero (C311)

## 1. Introducción al problema y búsqueda de una posible solución
Como bien el título ya da a entender, nuestra propuesta es un Simulador de Civilizaciones, a partir del uso de herramientas de las tres asignaturas. Nuestra idea inicial es hacerlo por capas de trabajo, donde desarrollaremos una serie de características y funcionalidades al programa una vez la base del proyecto esté completa.

La idea base del proyecto es la siguiente:
1. Crear un simulador que nos permita analizar el comportamiento de una civilización, dadas las condiciones de un terreno, y su evolución con el paso del tiempo.
2. La civilización estará dotada de una serie de variables que explican su funcionamiento y avance, dígase el índice de mortalidad, natalidad, gestación, promedio de vida, avance tecnológico, potencial adaptativo (dependiendo del medio ambiente definido), etc, y estará dotada de un comportamiento, dígase tendencia de movimiento, agresividad, actividades laborales principales, etc. 
3. Igualmente será posible establecer especies de menor o mayor alcance con respecto a una civilización, o sea, será posible establecer a especies atrasadas (ejemplo: moluscos, artrópodos, etc), especies intermedias (ejemplo: perros, gatos) yuna especie avanzada(ejemplo: humanos). 

La idea no es que se establezcan en el nivel según los ejemplos anteriores, sino que, a partir de un lenguaje definido por nosotros y un compilador para el mismo, puedan ser creadas especies con gran cantidad de características, incluso que el usuario defina el comportamiento de la mayor parte de las variables.

Propondremos realizar la evolución de la civilización en el tiempo utilizando herramientas de inteligencia artificial, así como el uso de estas herramientas en otras partes del trabajo a medida que avancemos.Una vez que cumplamos con la base de nuestro simulador, nos tomaremos como meta lograr las siguientes ideas por capas:
* Implementar un sistema de desastres naturales, dígase huracanes, terremotos, etc.
* Implementar un sistema de enfermedades naturales, ya hereditarias, infecciosas.
* Implementar un sistema de ambientación. Esto incluirá terrenos con características climáticas, estaciones, etc.-Implementar la posibilidad de permitir diferentes intervalos de tiempos de avance en la simulación (ejemplo: días, semanas, meses, años, décadas, etc).
* Lograr la existencia de más de una civilización, lo cual da paso a establecer un sistema de interacción entre dos civilizaciones distintas (dígase problemas menores, guerras, alianzas, uniones, etc)
* Posibilitar la transición entre el estado de evolución de una especie, dígase de atrasado a intermedio, o de intermedio a civilizado.
* Habilitar la existencia de subgrupos dentro de una misma especie. Sectores dedicados a cierta parte de la civilización (ejemplo: obreros, filósofos, artesanos, etc), grupos problemáticos, grupos desertores, etc.
* Habilitar la evolución de las enfermedades, adaptación, surgimiento, cambio (tanto de enfermedades hereditarias como infecciosas).
* Habilitar el cambio climático y evolución de este.Si bien el anterior orden de las capas de trabajo no es definitivo, en un primer momento esperaríamos fluyera de esa forma.

Queremos ser capaces de lograr que todas las capas de trabajo mencionadas puedan ser generadas a partir del lenguaje por el usuario (crear especies, subgrupos, desastres, enfermedades, etc) con las variables y evolución de las mismas que se estime conveniente.

El lenguaje, aún no definido claro está, lograremos que no se limite a la creación de la simulación, sinoquetambién pueda ser capaz de modificar dinámicamente el comportamiento y evolución de todo lo que es posible implementar en esta simulación.

Concretamente queremos crear un software que a nivel de problaciones de especies en un ambiente definido pueda simular el desarrollo de las mismas de tal manera que podamos obtener,a través de técnicas de visualización, las estadísticas de losparámetros de interés en eltiempo y espacio que querramos conociendo todas las interacciones entre la disímiles especiesy/o poblacionesy el medio en que encuentran, además un entorno controlable en cualquier momento a partir del lenguaje creado específicamente para nuestro problema.

Espereamos la idea sea de su agrado, muchas gracias.

## 2. Primeros pasos
Se ha implementado un prototipo inicial del proyecto en el que esta definida tres clases principales: Specie, Land y Simulation. Estas componen las escencia de lo que se espera como producto final. 
Specie define cada especie por separado, esta consta con un nombre, una lista de características(las que tienen por valor un número o un rango), y otra de dependencias entre las mismas donde podemos definir las relaciones entre las características de la siguiente forma: 
    a -> b * c 
Al pasar un día en la simulación esta dependencia es expresada de la siguienteforma: 
    b += a * c

Land define una parte del terreno, esta consta de una lista de características, y otra de dependencias siguiendo la misma lógica vista anteriormente

Simulation se encarga de contener el terreno, crear las especies, además esta debe contener las reglas de nuestro sistema y de acuerdo a a las mismas correr las simulación.

### 2.1 Problemáticas principales
Definir las reglas sobre como va a estar distribuido las especies en el terreno y las consecuencias de tal forma que si crece la población como se ditribuye en el terreno, o si lo hacemos región a región

Otra problemática principal es como definir las interrelaciones terreno - terreno, especie - especie, terreno - specie, specie - terreno. Puesto que solo definimos las dependencias entre la misma especie o terreno, pero como definimos entre instancias diferentes o entre terrenos y especies. este problema necesita más debate entre los desarrolladores y se espera llegar a un consenso en el próximo paso

Definir las reglas de nuestra simulación que no son modificables por el usuario, vitales para un correco funcionamiento del sistema. 

### 2.2 Proximos pasos
Lograr un consenso para definir la resolución de las problemáticas y llevarlo al proyecto.

Tener una primera gramática y lograr un avance significativo en la defición del lenguaje a usar por el usuario, así como el tokenizador, parser, etc

Implementar las funciones de distribución a usar dado que actualmente solo se hace un random por defecto y por supuesto eso se debe mejorar.

Perfeccionar la simulación dado que esta corre aplicando als dependencias una a una, pero no como un conjunto que sucede todo al mismo tiempo, creemos que ir introduciendo ecuaciones diferenciales nos puede ayudar a lograrlo

Crear estructuras y algoritmos para una optimización de lo ya implementado