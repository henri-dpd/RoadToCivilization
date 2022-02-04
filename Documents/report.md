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

## 3. Restructurando mundo, implementando reglas y adaptando estructura por capas.

En esta iteracion se ha avanzado en resolver las problematicas encontradas en el anterior modelado del problema conllevnado consigui una restrucutracion parcial del proceto, un cambio de filosofia en la implememtacion.

### 3.1. Primeros cambios 
#### Nuevo:
* Concepto de sociedad como unidad atomica, agente en esta simulacion que busca supervivencia, esta pertenece a una unica especie y se ubica en un unico terreno.
* Concepto de influencia, dado que las dependencias son hechos que ocurren en un inervalo de tiempo, es necesario tener un hecho que represente una correspondencia entre dos caracteristicas de tal manera que cuando una cambie la otra cambie proporcional al cambio de la primera. Ejemplo: A mayor economia, menor hambre. Como dependencia este no se podria representar dado que solo logramos que en cada iteracion aumente proporcional a toda la economia, ahora con influencias logramos una correcta modelacion de la problematica dado que hambre aumenta o disminuye propoircional al cambio que tenga la economia esa iteracion. 
* Limites en las caracteristicas, importante para lograr una facil y correcta modelacion de algunas caracteristicas por ejemplo la cantidad de los recursos o el agua dado que no puede ser menor que 0.
* Lista de entidades por terreno, en la que guardamos todas las entidades que interactuan en el mismo.
* Lista de operaciones y distribuciones en la que guardamos las operaciones que se hacen entre caracteristicas(dependencias, influencias), y las distribuciones que se calculan al trabajar en los rangos.
#### Cambios:
* Specie reconvertido a un simple contenedor por ahora, el objetivo es que persista como concepto global, que se pueda apoyar en ello para obtener las salidas a estudiar pero que como tal no tenga como generar ninguna accion en la simulacion.
* Redefinicion de los conceptos de dependencias e interdependencias, dependencias son todas las dependencias e influecias que ocurren a nivel de terreno, ya sea en el mismos terrenos, en una sociedad o entre sociedades o sociedad - terreno, interdependenias son todo cambio que ocurre a nivel de simulacion, de terreno a terreno(entre los mismos terrenos o sus sociedades)
* Calculo de dependencias usando la lista de operaciones y distribuciones.
* Resuelto problemas de importancia de orden de las dependecias al calcular el move_one_day.
### 3.2 Mejorias de los cambios
Tras esta nueva iteracion se vienen varias mejoras, empezando con la inclusion del concepto sociedad y reestructuracion del proyecto dado que primeramente resuleve el problema de que las especies actuaban en general, no habia diferencias de cuantos pudieran estar en un terreno y las consecuencias que esto implica con respecto a las inter-dependencias, esto representaba una inconsistencia que con la inclusion de las sociedades queda resuleto, ademas tenemos una estructura mas solida, y las socedades se convierten asi en la unidad atomica del proyecto sobre las que queremos construir el concepto de agentes en busca de superviviencia. 

Ademas se agrega dos conceptos de suma importancia para darle la libertad al usuario de escribir un modelo mas acorde a lo que se espera teniendo dos reglas a su disposicion como son las influencias y los limites explicados anteriormente.

Tambien se resuleve un problema que es la imporancia del orden de las dependencias a la hora de ejecutar el metodo move_one_day, esto hace que sea una simulacion mas justa dado que en este modelo todo no puede pasar al mismo tiempo al menos nos olvidamos de que orden se van calculando las dependencias y que este influyene en la simulacion o no, solo bastaba con gurdar los cambios en una lista aparte y luego actualizarlo.

Otro importante cambio fue en la construccion de lista de operaciones para calcular las dependencias e influencias lo que nos permite una mayor abstraccion dando paso que el usuario pueda definir su propia operacion o distribucion y annadirla a la la lista para luego usarla.

Especies ahora es un objeto abstracto, que es completamente dependiente de las sociedades de la misma que exista en ese momento. Esto nos ofrece la posibilidad de poder actuar y revisar las especies de forma mas general independiente del lugar en que pueda encontrar sociedades.

### 3.3 Proximos pasos
* Terimanr el compilador
* Implementar Mutacion y Migracion
