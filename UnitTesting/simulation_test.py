import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth

path.append(str(Path(__file__).parent.parent.absolute()))

from simulation import Simulation


@pytest.mark.parametrize('col, row, res1, res2, res3, res4',
                        [
                           (3,3,3,3,[],[]),  
                           (2,3,2,3,[],[]),  
                           (4,3,4,3,[],[])  
                        ]
                        )

def test_simulation_creation(col, row, res1, res2, res3, res4) -> None:
    # Crear Simuladior y checkear atributos
    sim = Simulation(row, col)
    assert sim.columns == res1
    assert sim.rows == res2
    assert sim.actual_species == res3
    assert sim.inter_dependences == res4
    
@pytest.mark.skip()
def test_simulation_redimention_map_values() -> None:
    # Crear Simuladior, redimencionar y checkear atributos
    sim = Simulation(2,3)
    sim.Re_Dimention_Map(4,5)
    assert sim.columns == 5
    assert sim.rows == 4    
    sim.Re_Dimention_Map(1,2)
    assert sim.columns == 2
    assert sim.rows == 1
    sim.Re_Dimention_Map(3,1)
    assert sim.columns == 1
    assert sim.rows == 3
    sim.Re_Dimention_Map(2,4)
    assert sim.columns == 4
    assert sim.rows == 2


@pytest.mark.skip()
def test_simulation_add_delete_species() -> None:
    sim = Simulation(2,3)
    
    #Testeando annadir
    res1 = False
    res2 = False
    sim.Add_Species('Humano')    
    sim.Add_Species('Marciano')    
    for actual in sim.actual_species:
        if actual.name == 'Humano':
            res1 = True            
        if actual.name == 'Marciano':
            res2 = True    
    assert res1
    assert res2    
    res1 = False
    res2 = False
    res3 = False
    for i in range(10000):
        sim.Add_Species('Humano')    
    sim.Add_Species('Yedi')    
    for actual in sim.actual_species:
        if actual.name == 'Humano':
            res1 = True            
        if actual.name == 'Marciano':
            res2 = True            
        if actual.name == 'Yedi':
            res3 = True    
    assert res1 
    assert res2
    assert res3
    assert len(sim.actual_species)==3
    
    #Testeando eliminar
    assert sim.Delete_Species(20) ==0
    assert len(sim.actual_species)==3
    assert sim.Delete_Species(-1) ==0
    assert len(sim.actual_species)==3
    
    sim.Delete_Species(1)
    res1 = False
    res2 = False
    res3 = True
    sim.Add_Species('Humano')    
    sim.Add_Species('Yedi')    
    for actual in sim.actual_species:
        if actual.name == 'Humano':
            res1 = True            
        if actual.name == 'Yedi':
            res2 = True    
        if actual.name == 'Maarciano':
            res3 = False    
    assert res1 
    assert res2
    assert res3
    assert len(sim.actual_species)==2
