import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
import logging

path.append(str(Path(__file__).parent.parent.absolute()))

from land import Land
from species import Species

def test_land() -> None:
    logging.basicConfig(filename='land_test.log', filemode='w', format='%(levelname)s ~ %(asctime)s -> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

     #Creando Land y poniendo caracteristicas por defecto
    terreno = Land([0,0])
    assert terreno.characteristic == {}
    assert terreno.characteristic_dependences == []
    
    terreno.Set_Default_Characteristics()
    assert len(terreno.characteristic) == 6
    
    #Testeando caracteristicas
    assert terreno.Get_Characteristic_Value('Recursos Actuales') == 1
    terreno.Change_Characteristic('Recursos Actuales', 500, 0, 21000)
    assert terreno.Get_Characteristic_Value('Recursos Actuales') == 500
    
    assert len(terreno.characteristic) == 6
    terreno.Delete_Characteristic('Recursos Actuales')
    assert len(terreno.characteristic) == 5
    assert 'resources_capacity' not in terreno.characteristic
    terreno.Delete_Characteristic('Recursos Actuales')
    assert len(terreno.characteristic) == 5
    
    terreno.Change_Characteristic('Recursos Actuales', 1000)
    assert terreno.Get_Characteristic_Value('Recursos Actuales') == 1000
    assert len(terreno.characteristic) == 6
    
    #Testeando dependencias
    terreno.Add_Dependence('','Altitud', '','Temperatura', 1)
    assert len(terreno.characteristic_dependences) == 1
    terreno.Add_Dependence('','Fertilidad', '','Recursos Actuales', 20)
    assert len(terreno.characteristic_dependences) == 2
    terreno.Add_Dependence('', 'Fertilidad', '', 'Recursos Actuales', 20)
    assert len(terreno.characteristic_dependences) == 2
    #orden de las dependencias
    terreno.Add_Dependence('', 'Recursos Actuales','',  'Fertilidad', 10)
    assert len(terreno.characteristic_dependences) == 3
    terreno.Delete_Dependence('','Altitud', '','Temperatura')
    assert len(terreno.characteristic_dependences) == 2
    
    terreno.Change_Dependences_Value('','Recursos Actuales','', 'Fertilidad', 0.001)
    assert terreno.characteristic_dependences[1].c == 0.001
    
    terreno.Delete_Dependence('', 'Altitud', '', 'Temperatura')
    assert len(terreno.characteristic_dependences) == 2
    
    terreno.Add_Dependence('', 'Recursos Actuales', '', 'Recursos Actuales', 0.005)
    assert len(terreno.characteristic_dependences) == 3
    assert terreno.characteristic_dependences[2].c == 0.005
    
    terreno.Add_Influences('','Altitud', '', 'Temperatura', 5)
    terreno.Add_Influences('','Fertilidad','', 'Nivel de Acogimiento', 5)
    assert len(terreno.characteristic_influences) == 2
    assert terreno.Get_Characteristic_Value('Recursos Actuales') == 1000
    assert terreno.Move_One_Day() == None
    assert terreno.Get_Characteristic_Value('Recursos Actuales') > 500
    for i in range(1000):
        assert terreno.Move_One_Day() == None
    #Altura no cambia por lo tanto temperatura se mantiene igual aunque este influenciado por la altura
    assert terreno.Get_Characteristic_Value('Temperatura') == [0,1]
    assert terreno.Get_Characteristic_Value('Recursos Actuales') > 20000
    assert terreno.Get_Characteristic_Value('Fertilidad')[0] > 5000 and terreno.Get_Characteristic_Value('Fertilidad')[1] > 5000
    #Aqui sin embargo nivel de acogimiento esta influenciado por fertilidad, 
    #como fertilidad cambia significativamente el nivel de acogimiento tambien
    assert terreno.Get_Characteristic_Value('Nivel de Acogimiento') > 40000
    
    terreno.Add_Society("Cuba", Species("Humanos"))
    terreno.Delete_Society("Cuba")
    terreno.Add_Society("Cuba", Species("Homo-sapiens"))
    
    terreno.Set_Default_Entities_Characteristic("Cuba")
    terreno.Add_Dependence("Cuba", "Poblacion", "Cuba", "Poblacion", 100)
    
    terreno.Add_Dependence("Cuba", "Poblacion", "", "Altitud", 2)
    assert terreno.Get_Characteristic_Value('Altitud') == 1
    assert terreno.Move_One_Day() == None
    assert terreno.Get_Entities_Characteristic_value("Cuba","Poblacion") == 1010
    assert terreno.Get_Characteristic_Value('Altitud') == 21
    assert terreno.Move_One_Day() == None
    assert terreno.Get_Entities_Characteristic_value("Cuba","Poblacion") == 102010
    assert terreno.Get_Characteristic_Value('Altitud') == 2041