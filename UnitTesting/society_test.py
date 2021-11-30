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
    
    china = Society('China', "Humanos")
    assert china.name == 'China'
    assert china.characteristic == {}
    assert china.characteristic_dependences == []
    
    china.Set_Default_Characteristics()
    assert len(china.characteristic) == 13    
    
    china.Change_Characteristic('population', 220)
    assert china.Get_Characteristic_Value('population') == 220
    