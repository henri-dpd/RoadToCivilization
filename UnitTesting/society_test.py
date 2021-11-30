import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
import logging

path.append(str(Path(__file__).parent.parent.absolute()))

from society import Society

def test_society() -> None:
    logging.basicConfig(filename='society_test.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

     #Creando society y poniendo caracteristicas por defecto
    cuba = Society('Cuba', "Humanos")
    assert cuba.name == 'Cuba'
    assert cuba.characteristic == {}
    assert cuba.characteristic_dependences == []
    
    cuba.Set_Default_Characteristics()
    assert len(cuba.characteristic) == 13
    
    #Testeando caracteristicas
    assert cuba.Get_Characteristic_Value('population') == 1
    cuba.Change_Characteristic('population', 100, 0, 5000)
    assert cuba.Get_Characteristic_Value('population') == 100
    
    assert len(cuba.characteristic) == 13
    cuba.Delete_Characteristic('actual_growth')
    assert len(cuba.characteristic) == 12
    assert 'actual_growth' not in cuba.characteristic
    cuba.Delete_Characteristic('actual_growth')
    assert len(cuba.characteristic) == 12
    
    cuba.Change_Characteristic('politics', 10000)
    assert cuba.Get_Characteristic_Value('politics') == 10000
    assert len(cuba.characteristic) == 13
    
    #Testeando dependencias
    cuba.Add_Dependences('population', 'gestation', 0.5)
    assert cuba.characteristic_dependences == [['population', 'gestation', 0.5]]
    cuba.Add_Dependences('population', 'gestation', 1)
    assert cuba.characteristic_dependences == [['population', 'gestation', 0.5]]
    cuba.Add_Dependences('gestation', 'birth_rate', 0.01)
    assert cuba.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 0.01]]
    #orden de las dependencias
    cuba.Add_Dependences('birth_rate', 'gestation', 0.015)
    assert cuba.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 0.01],['birth_rate', 'gestation', 0.015]]
    cuba.Delete_Dependences('birth_rate', 'gestation')
    
    #orden de las dependencias
    cuba.Change_Dependences_Value('birth_rate', 'gestation', 200)
    assert cuba.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 0.01]]    
    cuba.Change_Dependences_Value('gestation', 'birth_rate', 2)
    assert cuba.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 2]]    
    cuba.Change_Dependences_Value('population', 'birth_rate', 2)
    assert ['population', 'birth_rate', 2] not in cuba.characteristic_dependences
    
    cuba.Delete_Dependences('population', 'gestation')
    assert cuba.characteristic_dependences == [['gestation', 'birth_rate', 2]]
    cuba.Delete_Dependences('population', 'gestation')
    assert cuba.characteristic_dependences == [['gestation', 'birth_rate', 2]]
    cuba.Delete_Dependences('population', 'birth_rate')
    assert cuba.characteristic_dependences == [['gestation', 'birth_rate', 2]]
    
    cuba.Add_Dependences('birth_rate', 'population', 3.5)
    assert cuba.characteristic_dependences == [['gestation', 'birth_rate', 2],['birth_rate', 'population', 3.5]]
    
    cuba.Delete_Dependences('gestation', 'birth_rate')
    cuba.Add_Dependences('population', 'population', 10)
    assert cuba.characteristic_dependences == [['birth_rate', 'population', 3.5],['population', 'population', 10]]
    
    assert cuba.Move_One_Day() == None
    assert cuba.Move_One_Day() == None
    assert cuba.Move_One_Day() == None
    assert cuba.Get_Characteristic_Value('population') > 100
    
    china = Society('China', "Humanos")
    assert china.name == 'China'
    assert china.characteristic == {}
    assert china.characteristic_dependences == []
    
    china.Set_Default_Characteristics()
    assert len(china.characteristic) == 13    
    
    china.Change_Characteristic('population', 220)
    assert china.Get_Characteristic_Value('population') == 220
    china.Add_Dependences('economy', 'population', 0.2)
    assert china.characteristic_dependences == [['economy', 'population', 0.2]]
    assert china.Move_One_Day() == None
    assert china.Get_Characteristic_Value('population') > 220
    
    
    cuba.Add_Influences('gestation', 'birth_rate', 0.1)
    cuba.Add_Influences('intellect', 'size', 5000)
    cuba.Add_Dependences('population', 'economy', 0.002)
    cuba.Add_Dependences('economy', 'gestation', 0.04)
    for i in range(1000):
        assert cuba.Move_One_Day() == None
    
    #Población no cambia dado que tiene un límite, pero la dependencia trata el valor, no el cambio que sufre
    assert cuba.Get_Characteristic_Value('population') > 4999
    assert cuba.Get_Characteristic_Value('economy') > 10000
    assert cuba.Get_Characteristic_Value('gestation') > 10000
    #Economia cambia por la dependencia, tambien cambia gestación por dependencia de economía,
    # y estos cambios en gestación son reflejados en rango de nacimiento por la influencia
    assert cuba.Get_Characteristic_Value('birth_rate')[0] > 5000 and cuba.Get_Characteristic_Value('birth_rate')[1] > 5000
    #Aqui sin embargo tamaño esta influenciado por inteligencia, 
    #como inteligencia no cambia el valor el tamaño tampoco 
    assert cuba.Get_Characteristic_Value('size') == 1
    