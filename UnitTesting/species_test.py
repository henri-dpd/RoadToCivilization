import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth

path.append(str(Path(__file__).parent.parent.absolute()))

from species import Species

def test_species() -> None:
    #Creando especies y poniendo caracteristicas por defecto
    humano = Species('Humano')
    assert humano.name == 'Humano'
    assert humano.characteristic == {'population':1}
    assert humano.characteristic_dependences == []
    
    humano.Set_Default_Characteristics()
    assert len(humano.characteristic) == 13
    
    #Testeando caracteristicas
    assert humano.characteristic['population'] == 1
    humano.Change_Characteristic('population', 50)
    assert humano.characteristic['population'] == 50
    
    assert len(humano.characteristic) == 13
    humano.Delete_Characteristic('size')
    assert len(humano.characteristic) == 12
    assert 'size' not in humano.characteristic
    humano.Delete_Characteristic('size')
    assert len(humano.characteristic) == 12
    
    humano.Change_Characteristic('size', 2)
    assert humano.characteristic['size'] == 2
    assert len(humano.characteristic) == 13
    
    #Testeando dependencias
    humano.Add_Dependences('population', 'gestation', 0.5)
    assert humano.characteristic_dependences == [['population', 'gestation', 0.5]]
    humano.Add_Dependences('population', 'gestation', 1)
    assert humano.characteristic_dependences == [['population', 'gestation', 0.5]]
    humano.Add_Dependences('gestation', 'birth_rate', 0.01)
    assert humano.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 0.01]]
    #orden de las dependencias
    humano.Add_Dependences('birth_rate', 'gestation', 0.015)
    assert humano.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 0.01],['birth_rate', 'gestation', 0.015]]
    humano.Delete_Dependences('birth_rate', 'gestation')
    
    #orden de las dependencias
    humano.Change_Dependences_Value('birth_rate', 'gestation', 200)
    assert humano.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 0.01]]    
    humano.Change_Dependences_Value('gestation', 'birth_rate', 2)
    assert humano.characteristic_dependences == [['population', 'gestation', 0.5],['gestation', 'birth_rate', 2]]    
    humano.Change_Dependences_Value('population', 'birth_rate', 2)
    assert ['population', 'birth_rate', 2] not in humano.characteristic_dependences
    
    humano.Delete_Dependences('population', 'gestation')
    assert humano.characteristic_dependences == [['gestation', 'birth_rate', 2]]
    humano.Delete_Dependences('population', 'gestation')
    assert humano.characteristic_dependences == [['gestation', 'birth_rate', 2]]
    humano.Delete_Dependences('population', 'birth_rate')
    assert humano.characteristic_dependences == [['gestation', 'birth_rate', 2]]
    
    humano.Add_Dependences('birth_rate', 'population', 3.5)
    assert humano.characteristic_dependences == [['gestation', 'birth_rate', 2],['birth_rate', 'population', 3.5]]
    
    #No lo agrega, error o a proposito
    humano.Add_Dependences('population', 'population', 10)
    assert humano.characteristic_dependences == [['gestation', 'birth_rate', 2],['birth_rate', 'population', 3.5],['population', 'population', 10]]
    humano.Delete_Dependences('population', 'population')
    
    assert humano.Move_One_Day() == None
    assert humano.characteristic['population'] > 50
    