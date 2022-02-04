import pytest
from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth
import logging

path.append(str(Path(__file__).parent.parent.absolute()))

from simulation import Simulation
from land import Land
from society import Society
from evolution import Evolution

def test_evolution() -> None:

    sim = Simulation(2,2)
    sim.Add_Species("Humano")
    sim.Add_Society(0, 0, "Cubano", "Humano")
    sim.Add_Society(0, 0, "Español", "Humano")
    sim.Add_Society(1, 1,"Americano", "Humano")
    sim.map[0][0].entities["Español"].enable_evolution = False
    sim.map[1][1].entities["Americano"].enable_evolution = False
    sim.Change_Society_Characteristic(0,0, "Español", "Población", 3)
    sim.Change_Society_Characteristic(0,0, "Cubano", "Población", 10)
    sim.Change_Society_Characteristic(0, 0, "Cubano", "Economía", 10)
    sim.Change_Society_Characteristic(0, 0, "Cubano", "Coronavirus", -5)
    sim.Add_Land_Dependences(0, 0 , "Cubano", "Economía", "Cubano", "Población", 1)
    sim.Add_Land_Dependences(0, 0 , "Español", "Población", "Cubano", "Economía", 1)
    sim.Add_Inter_Dependence([1,1], "Americano", "Población", [0,0], "Cubano", "Población", -1)
    sim.Move_One_Day_All()
    print(sim.map[0][0].entities["Cubano"].evolution)