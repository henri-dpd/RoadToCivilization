import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
import logging
import math

path.append(str(Path(__file__).parent.parent.absolute()))

from society import Society
from species import Species

def test_society() -> None:
    logging.basicConfig(filename='society_test.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

     #Creando society y poniendo caracteristicas por defecto
    humanidad = Species("Humano")
    cuba = Society('Cuba', humanidad)
    assert cuba.name == 'Cuba'
    assert cuba.Get_Characteristic_Value('Población') == 10
    
    cuba.Set_Default_Characteristics()
    assert len(cuba.characteristic) == 13
    
    #Testeando caracteristicas
    assert cuba.Get_Characteristic_Value('Población') == 10
    cuba.Change_Characteristic('Población', 100, 0, 5000)
    assert cuba.Get_Characteristic_Value('Población') == 100
    
    assert len(cuba.characteristic) == 13
    cuba.Delete_Characteristic('Crecimiento Actual')
    assert len(cuba.characteristic) == 12
    assert 'Crecimiento Actual' not in cuba.characteristic
    cuba.Delete_Characteristic('Crecimiento Actual')
    assert len(cuba.characteristic) == 12
    
    cuba.Change_Characteristic('politics', 10000)
    assert cuba.Get_Characteristic_Value('politics') == 10000
    assert len(cuba.characteristic) == 13
    
    china = Society('China', humanidad)
    assert china.name == 'China'
    assert china.Get_Characteristic_Value('Población') == 10
    
    china.Set_Default_Characteristics()
    assert len(china.characteristic) == 13    
    
    china.Change_Characteristic('Población', 220)
    assert china.Get_Characteristic_Value('Población') == 220
    