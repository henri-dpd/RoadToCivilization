import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
import logging

path.append(str(Path(__file__).parent.parent.absolute()))

from species import Species

def test_species() -> None:
    logging.basicConfig(filename='specie_test.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    #Creando especies y poniendo caracteristicas por defecto
    humano = Species('Humano')
    assert humano.name == 'Humano'
    assert humano.characteristic == {}
    
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
    
    
    alien = Species('Alien')
    assert alien.name == 'Alien'
    assert alien.characteristic == {}
    
    alien.Set_Default_Characteristics()
    assert len(alien.characteristic) == 13    
    
    alien.Change_Characteristic('population', 220)
    assert alien.characteristic['population'] == 220
    
    