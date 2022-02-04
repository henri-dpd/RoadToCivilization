# Propuesta a Lenguaje de Road to Civilization

La idea central es que sea un lenguaje parecido a C#, donde puedas hacer en primera instancia las cosas básicas de este lenguaje.

``` c
Type name = value;
```
Será la sintaxis para declarar una variable

Las estructuras de control serán iguales:
``` c
If(conditions)
{	Code;    }
/* Elif(conditions)
{	Code;    } */
Else
{	Code;    }
```
Excepto que en C# no existe elif pero aquí sí.

Las condiciones pueden usar indistintamente "and", "or" y "not", y los comparadores serían <, >, <=, >=, ==, !=

Entonces, tendremos igualmente el while y for trabajando de la misma forma:
``` c
While(conditions) {         Code       }
/* For(init, conditions, operations) {     Code    } */
```
Todo con sus respectivos continue y break.

Las funciones se declaran especificando el tipo de las variables de retorno, así como el tipo de las variables de entrada.
``` c
Type name(type value_1, type value_2, …)
{
	Code;
	Return value_n;
}
```

Igualmente se puede hacer: 
``` c
Type name(type value_1, type value_2, …) = value
```
Que básicamente indica que lo que se guarda en name es una función que recibe los parámetros descritos y devuelve el Type descrito, en caso de que value sea una constante y no una función, entonces simplemente devuelve esa constante (si coincide con el tipo descrito en el retorno).

Los tipos que soportará el lenguaje serán los int, double,<!--  char, --> string y bool, todos funcionan y se declaran igual que en C#, así como realizan las operaciones idéntico a C#, incluso los casting.

Las estructuras de datos que soportará el lenguaje son las<!--  tuplas, --> listas y arrays multidimensionales. En el caso de los arrays de una dimensión<!-- , tendrán los métodos oportunos para poder ser tratados como colas o pilas -->

Se Declaran de la siguiente forma:
``` c
/* Tuple<types> name = (value_1, value_2,…); */
List<type> name = [value_1, value_2, …];
List<List<type>> name = [[value_1, value_2,…],
			[value_1, value_2,…]];
```
<!-- Sin embargo, también agregamos un tipo a esta simulación, que es el interval, que se puede declarar de dos formas:
```c#
Interval name = [value_1, value_2]
Int[2] name = [value_1, value_2]
```
Básicamente representa un intervalo con un mínimo y un máximo.
Como siempre se indexa de la forma [index_1, index_2, …], tanto para indexar como para asignar -->


Ahora, con respecto a la simulación en general.
Para colocar una nueva especie se necesita lo siguiente:
``` c
Name = Species(“Especie_name”)
``` 
O así mismo recibir un string o char por argumento.

Para hacer un nuevo Land se necesita lo siguiente:
``` c
Name = Land(“Land_name”)
```
Y para Sociedad:
``` c
Name = Society(“Society_name”)
```

Una vez dicho esto pasamos directamente a cómo se define la simulación.
Siempre va a existir una simulación llamada directamente Simulation, que es la simulación principal.

Las comandos para interactuar con Simulation son:
Redimension(value_1, value_2), donde ambos parámetros deben ser int.
Start, no recibe parámetros e inicia la simulación
End, esta será explicada más adelante
Restart,no recibe parámetros devuelve la simulación a su estado inicial (antes de último Start)
Erase, no recibe parámetros, y es equivalente a hacer Redimension(0,0)

Igualmente está una biblioteca que implementamos por detrás, la biblioteca Random, a la que se accede mediante Random.random_name, todas estas funciones reciben dos parámetros por entrada estas funciones, que son el límite inferior y superior, o media y variancia, y devuelven el valor del random descrito evaluado en ese intervalo.
Ejemplo:
``` c
Int a = Random.Normal(0, 5)
```

Ahora solo nos resta hablar de cómo funciona las características, dependencias e interdependencias.
Consideremos una Species, Land o Society como un entity.

Para agregar una característica a Land, Society o Species se hace de la siguiente forma:
Entity.Characteristic_A = [value, mut, button, top, distribution], donde value debe ser un int, double o un interval, mut(omitible) es la mutabilidad representado por un entero, button y top son los límites(se puede omitir) representados por enteros, y por ultimo la ditribución(omitible) representado por una funcion. Por defecto mut = 1, button = -inf, top = int, distribution = random.default(). 
La única excepción es con Species_A.Population, que siempre debe ser un int, y es la única característica definida de antemano al crear una especie, por defecto en 1.

Dicho todo esto solo nos resta explicar el cómo establecer una interdependencia o dependencia.
La sintaxis especial para esto es el =>. 
``` c
Entity_1.Characteristic_A => Entity_2.Characteristic_B * C 
{
	pos1 = [1,2];
	pos2 = [1,2];
}
```
Así se declara una dependencia que se traduce literalmente como:
``` c
Characteristic_B = Characteristic_B + Characteristic_A * C
{
	pos1 = [1,2];
	pos2 = [1,2];
}
```
Las influencias son declaradas de la misma forma solo ccon la diferencia de que el oprador es ~> quedando en el codigo de la siguiente forma
``` c
Entity_1.Characteristic_A ~> Entity_2.Characteristic_B * C
{
	pos1 = [1,2];
	pos2 = [1,2];
}
```
Ojo:
Dentro de Land pueden existir varios Society, por tanto:
Land_A.Society_B es la forma de acceder al Society deseado dentro de Land.
Lo mismo pasa con la sintaxix:
Land_A.Species_B, que en este caso afecta a la característica que tenga toda Sociedad de la Especie B dentro del Land A.
Entonces, falta el cómo poder modificar la dependenciao influencia, pues se hace de la siguiente forma (durante su definición)
``` c
Entity_1.Characteristic_A => Entity_2.Characteristic_B * C {
	pos1 = [1,2];
	pos2 = [1,2];
	sum = function_1;
	mul = function_2;
}
```

<!-- Using * = Funtion_1
Using + = Funtion_2
Using $ = Funtion_3
With A = Random.random_1
With B = Random.random_2
With C = Random.random_3

Ahora, qué quiere decir esta sintaxis:
El Using se utiliza (valga la redundancia) para modificar las funciones * y + de la dependencia, existen 3, el * (que modifica la función * de la fórmula), el + (que modifica la función + de la fórmula), y el \$, que modifica los dos a la vez.
Para estas funciones no se declaran parámetros de entrada, por defecto reciben variables de nombre A, B y C en dependencia de cuál es a la que nos referimos.
Si es *, recibe A y C, si es + recibe B y el resultado de la operación * en A y C, y si es \$, recibe los tres, A, B y C.
No se utilizar a la vez el Using \$ con alguno de los otros dos.
Estas funciones no tienen que ser declaradas en el momento (aunque pueden serlo), pueden apuntar a funciones ya realizadas anteriormente, pero estas deben ser siempre funciones que devuelvan int, y reciban en caso de + y * dos parámetros de tipo int y en caso de $ tres parámetros de tipo int. Este caso sería equivalente a llamar a la función que apunta con los parámetros designados A, B o C en orden alfabético.
En el caso de los With, simplemente describen con qué función de random se deduce el valor de A, B y C en caso de que estos hayan sido definidos como Interval por detrás.
``` -->

Quedando esto dicho, vamos ahora a ver qué podemos hacer mientras corre una simulación.

Es posible declarar código que trabajará mientras corre la simulación, esto se hace mediante la sintaxis:
``` c
Day number
{
	Code;
}
```
Donde number debe ser un entero, una variable, o una expresión de la forma nx, donde n es un número entero.
Si es un número n o apunta a una variable de valor n, pues significa que en el día n-ésimo de la simulación se ejecutará el código descrito, si es de la forma nx, significa que en todo día k de la forma n*x, con x =(0,1,2,3,4…), se ejecutará el código descrito.
Entonces, no se puede escribir comando en estas partes, solo los comandos del tipo:
-Writeline(value), que recibe un valor que puede ser bien dentro de la simulación, por ejemplo:
Writeline(Human.Population)
Y lo imprime en consola
-Record name(value), Que crea un archivo txt de nombre name y lo modifica guardando dentro el nombre de la variable value y su valor (en caso de existir el txt solo se agrega la información)
-End, la cual ya habíamos mencionado anteriormente.
End puede no recibir nada, y simplemente detiene la simulación (ojo, no la reinicia, solo no continua el contador de días ni avanzan las características), o puede recibir una condición con la palabra reservada when, por ejemplo:
``` c
End when Human.Population > 100 and Cows.Population > 50
```
Donde la Simulación termina en este momento.
Esta misma sintaxis usando el when se puede realizar para el caso de Day, de la forma:
``` c
Day when Human.Population > 100 and Cows.Population > 50
{
	Code;
}
```

Adicionalmente será posible definir dependencias e influencias que se ejecuten a partir de cierto día:

``` c
	Day number/condition
{
	Entity_1.Characteristic_A => Entity_2.Characteristic_B * C {
	pos1 = [1,2];
	pos2 = [1,2];
	sum = function_1; // sum es +
	mul = function_2; // mul es *
}
```
