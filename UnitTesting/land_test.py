import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth

path.append(str(Path(__file__).parent.parent.absolute()))

from land import Land

def test_land() -> None:
    #Creando Land y poniendo caracteristicas por defecto
    terreno = Land()
    assert terreno.characteristic == {}
    assert terreno.characteristic_dependences == []
    
    terreno.Set_Default_Characteristics()
    assert len(terreno.characteristic) == 6
    
    #Testeando caracteristicas
    assert terreno.characteristic['actual_resources'] == 1
    terreno.Change_Characteristic('actual_resources', 500)
    assert terreno.characteristic['actual_resources'] == 500
    
    assert len(terreno.characteristic) == 6
    terreno.Delete_Characteristic('resources_capacity')
    assert len(terreno.characteristic) == 5
    assert 'resources_capacity' not in terreno.characteristic
    terreno.Delete_Characteristic('resources_capacity')
    assert len(terreno.characteristic) == 5
    
    terreno.Change_Characteristic('resources_capacity', 1000)
    assert terreno.characteristic['resources_capacity'] == 1000
    assert len(terreno.characteristic) == 6
    
    #Testeando dependencias
    terreno.Add_Dependences('altitude', 'temperature', 1)
    assert terreno.characteristic_dependences == [['altitude', 'temperature', 1]]
    terreno.Add_Dependences('fertility', 'actual_resources', 20)
    assert terreno.characteristic_dependences == [['altitude', 'temperature', 1],['fertility', 'actual_resources', 20]]
    terreno.Add_Dependences('fertility', 'actual_resources', 20)
    assert terreno.characteristic_dependences == [['altitude', 'temperature', 1],['fertility', 'actual_resources', 20]]
    #orden de las dependencias
    terreno.Add_Dependences('actual_resources', 'fertility', 10)
    assert terreno.characteristic_dependences == [['altitude', 'temperature', 1],['fertility', 'actual_resources', 20],['actual_resources', 'fertility', 10]]
    terreno.Delete_Dependences('altitude', 'temperature')
    
    #orden de las dependencias
    terreno.Change_Dependences_Value('actual_resources', 'fertility', 0.001)
    assert terreno.characteristic_dependences == [['fertility', 'actual_resources', 20],['actual_resources', 'fertility', 0.001]]   
    
    terreno.Delete_Dependences('altitude', 'temperature')
    assert terreno.characteristic_dependences == [['fertility', 'actual_resources', 20],['actual_resources', 'fertility', 0.001]] 
    
    terreno.Add_Dependences('actual_resources', 'actual_resources', 0.005)
    assert terreno.characteristic_dependences == [['fertility', 'actual_resources', 20],['actual_resources', 'fertility', 0.001], ['actual_resources', 'actual_resources', 0.005]]
    
    assert terreno.Move_One_Day() == None
    assert terreno.Move_One_Day() == None
    assert terreno.characteristic['actual_resources'] > 500
    assert terreno.characteristic['fertility'][0] > 0 and terreno.characteristic['fertility'][1] > 1
    