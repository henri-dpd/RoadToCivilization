import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
import logging

path.append(str(Path(__file__).parent.parent.absolute()))

from land import Land

def test_land() -> None:
    logging.basicConfig(filename='land_test.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

     #Creando Land y poniendo caracteristicas por defecto
    terreno = Land()
    assert terreno.characteristic == {}
    assert terreno.characteristic_dependences == []
    
    terreno.Set_Default_Characteristics()
    assert len(terreno.characteristic) == 6
    
    #Testeando caracteristicas
    assert terreno.Get_Characteristic_Value('actual_resources') == 1
    terreno.Change_Characteristic('actual_resources', 500, 0, 21000)
    assert terreno.Get_Characteristic_Value('actual_resources') == 500
    
    assert len(terreno.characteristic) == 6
    terreno.Delete_Characteristic('resources_capacity')
    assert len(terreno.characteristic) == 5
    assert 'resources_capacity' not in terreno.characteristic
    terreno.Delete_Characteristic('resources_capacity')
    assert len(terreno.characteristic) == 5
    
    terreno.Change_Characteristic('resources_capacity', 1000)
    assert terreno.Get_Characteristic_Value('resources_capacity') == 1000
    assert len(terreno.characteristic) == 6
    
    #Testeando dependencias
    terreno.Add_Dependence('','altitude', '','temperature', 1)
    assert terreno.characteristic_dependences == [[('','altitude'), ('','temperature'), 1]]
    terreno.Add_Dependence('','fertility', '','actual_resources', 20)
    assert terreno.characteristic_dependences == [[('','altitude'), ('','temperature'), 1],[('','fertility'), ('','actual_resources'), 20]]
    terreno.Add_Dependence('', 'fertility', '', 'actual_resources', 20)
    assert terreno.characteristic_dependences == [[('','altitude'), ('','temperature'), 1],[('','fertility'), ('','actual_resources'), 20]]
    #orden de las dependencias
    terreno.Add_Dependence('', 'actual_resources','',  'fertility', 10)
    assert terreno.characteristic_dependences == [[('','altitude'), ('','temperature'), 1],[('','fertility'), ('','actual_resources'), 20],[('','actual_resources'), ('','fertility'), 10]]
    terreno.Delete_Dependence('','altitude', '','temperature')
    assert terreno.characteristic_dependences == [[('','fertility'), ('','actual_resources'), 20],[('','actual_resources'), ('','fertility'), 10]]
    
    terreno.Change_Dependences_Value('','actual_resources','', 'fertility', 0.001)
    assert terreno.characteristic_dependences == [[('','fertility'), ('','actual_resources'), 20],[('','actual_resources'), ('','fertility'), 0.001]]
    
    terreno.Delete_Dependence('', 'altitude', '', 'temperature')
    assert terreno.characteristic_dependences == [[('','fertility'), ('','actual_resources'), 20],[('','actual_resources'), ('','fertility'), 0.001]]

    terreno.Add_Dependence('', 'actual_resources', '', 'actual_resources', 0.005)
    assert terreno.characteristic_dependences == [[('','fertility'), ('','actual_resources'), 20],[('','actual_resources'), ('','fertility'), 0.001],[('', 'actual_resources'), ('', 'actual_resources'), 0.005]]
    
    terreno.Add_Influences('','altitude', '', 'temperature', 5)
    terreno.Add_Influences('','fertility','', 'cozy_level', 5)
    assert terreno.characteristic_influences == [[('','altitude'), ('','temperature'), 5],[('','fertility'), ('','cozy_level'), 5]]
    assert terreno.Get_Characteristic_Value('actual_resources') == 500
    assert terreno.Move_One_Day() == None
    assert terreno.Get_Characteristic_Value('actual_resources') > 500
    for i in range(1000):
        assert terreno.Move_One_Day() == None
    #Altura no cambia por lo tanto temperatura se mantiene igual aunque este influenciado por la altura
    assert terreno.Get_Characteristic_Value('temperature') == [0,1]
    assert terreno.Get_Characteristic_Value('actual_resources') > 20000
    assert terreno.Get_Characteristic_Value('fertility')[0] > 5000 and terreno.Get_Characteristic_Value('fertility')[1] > 5000
    #Aqui sin embargo nivel de acogimiento esta influenciado por fertilidad, 
    #como fertilidad cambia significativamente el nivel de acogimiento tambien
    assert terreno.Get_Characteristic_Value('cozy_level') > 40000
    
    terreno.Add_Society("Cuba", "Humanos")
    terreno.Delete_Society("Cuba")
    terreno.Add_Society("Cuba", "Homo-sapiens")
    
    terreno.Set_Default_Entities_Characteristic("Cuba")
    terreno.Add_Dependence("Cuba", "population", "Cuba", "population", 100)
    
    terreno.Add_Dependence("Cuba", "population", "", "altitude", 2)
    assert terreno.Get_Characteristic_Value('altitude') == 1
    assert terreno.Move_One_Day() == None
    assert terreno.Get_Entities_Characteristic_value("Cuba","population") == 101
    assert terreno.Get_Characteristic_Value('altitude') == 3
    assert terreno.Move_One_Day() == None
    assert terreno.Get_Entities_Characteristic_value("Cuba","population") == 10201
    assert terreno.Get_Characteristic_Value('altitude') == 205