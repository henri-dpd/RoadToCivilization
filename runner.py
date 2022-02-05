
import os
import pathlib
from shutil import ExecError
from Simulation.simulation import Simulation
from Simulation.species import Species
from Simulation.land import Land
from Simulation.society import Society
from Simulation.operators import uniform, exponential, gamma, normal, binomial, geometric
from Simulation.operators import distribution_default, default_sum, default_mul

sim = Simulation(1,1)

dayling = {}

def z_day(conditional, apply):
    dayling[conditional] = apply

ends = []

def Check_Valid_Positions(row, column):
    if row < 0 or column < 0 or row >= sim.rows or column >= sim.columns:
        return "Index out of range of the Simulation in Position = [" + str(row) + "," + str(column) + "]"
    else:
        return None

def z_end(conditional):
    ends.append(conditional)

def z_start():
    while True:
        sim.Move_One_Day_All()
        for cond in dayling:
            if cond():
                dayling[cond]()
        end = False
        for cond in ends:
            if cond():
                end = True
                break
        if end:
            break 
        
def execute(code):
    try:
        exec(code)
    except Exception as error:
        print(repr(error))

def z_write(document_name, text):
    file_path = pathlib.Path(__file__).parents.absolute() + "/output/" + document_name + ".txt"
    file = open(file_path, 'a')
    file.write(text)

def z_redimention(rows, columns):
    if rows < 0 or columns < 0:
        raise Exception("Index cannot be negatives")
    sim.Re_Dimention_Map(rows, columns)

def z_random(distribution, input):
    if distribution == "normal":
        return normal(input)
    
    elif distribution == "uniform":
        return uniform(input)
    
    elif distribution == "gamma":
        return gamma(input)
    
    elif distribution == "geometric":
        return geometric(input)
    
    elif distribution == "binomial":
        return binomial(input)
    
    elif distribution == "exponential":
        return exponential(input)
    
    else:
        return 0

def z_distribution(values):
    if len(values) == 1:
        return distribution_default(values[0])
    elif len(values) == 2:
        return distribution_default(values)
    else:
        raise Exception("Invalid Argument :" + str(values))

def z_plus(left, right):
    if len(left) == 1 and len(right)==1:
        return default_sum(left[0], right[0])
    elif len(left) == 2 and len(right)==2:
        return default_sum(left, right)
    elif len(left) == 1 and len(right)==2:
        return default_sum(left[0], right)
    elif len(left) == 2 and len(right)==1:
        return default_sum(left, right[0])
    else:
        raise Exception("Invalid Argument :" + str(left) + ' ' + str(right)) 

def z_multiplication(left, right):
    if len(left) == 1 and len(right)==1:
        return default_mul(left[0], right[0])
    elif len(left) == 2 and len(right)==2:
        return default_mul(left, right)
    elif len(left) == 1 and len(right)==2:
        return default_mul(left[0], right)
    elif len(left) == 2 and len(right)==1:
        return default_mul(left, right[0])
    else:
        raise Exception("Invalid Argument :" + str(left) + ' ' + str(right)) 

def z_addLand(land, row, column):
    check = Check_Valid_Positions(row, column)
    if check != None:
        raise Exception(check + ". Land cannot be added")
    sim.Add_Land_Copy(land, row, column)

def z_deleteLand(row, column):
    check = Check_Valid_Positions(row, column)
    if check != None:
        raise Exception(check + ". Land cannot be deleted")
    sim.Reset_Land(row, column)

def z_addSociety(society, row, column):
    check = Check_Valid_Positions(row, column)
    if check != None:
        raise Exception(check + ". Society cannot be added")
    sim.Add_Society_Copy(society, row, column)

def z_deleteSociety(society, row, column):
    check = Check_Valid_Positions(row, column)
    if check != None:
        raise Exception(check + ". Society cannot be added")
    sim.Delete_Society(society.name, row, column)
    
def z_addSpecies(species):
    sim.Add_Species_Copy(species)

def z_deleteSpecies(species):
    sim.Delete_Species(species.name)

def z_addDependence(pos_1, entity_1_name, characteristic_1_name,
                    pos_2, entity_2_name, characteristic_2_name, c, plus, mult):
    check = Check_Valid_Positions(pos_1[0], pos_1[1])
    if check != None:
        raise Exception(check + ". Dependence cannot be added")
    check = Check_Valid_Positions(pos_2[0], pos_2[1])
    if check != None:
        raise Exception(check + ". Dependence cannot be added")

    sim.Add_Inter_Dependence(pos_1, entity_1_name, characteristic_1_name,
                             pos_2, entity_2_name, characteristic_2_name, c, plus, mult)

def z_deleteDependence(pos_1, entity_1_name, characteristic_1_name,
                       pos_2, entity_2_name, characteristic_2_name):
    check = Check_Valid_Positions(pos_1[0], pos_1[1])
    if check != None:
        raise Exception(check + ". Dependence cannot be deleted")
    check = Check_Valid_Positions(pos_2[0], pos_2[1])
    if check != None:
        raise Exception(check + ". Dependence cannot be deleted")

    sim.Delete_Inter_Dependence(pos_1, entity_1_name, characteristic_1_name,
                                pos_2, entity_2_name, characteristic_2_name)

def z_addInfluence(pos_1, entity_1_name, characteristic_1_name,
                   pos_2, entity_2_name, characteristic_2_name, c, plus, mult):
    check = Check_Valid_Positions(pos_1[0], pos_1[1])
    if check != None:
        raise Exception(check + ". Influence cannot be added")
    check = Check_Valid_Positions(pos_2[0], pos_2[1])
    if check != None:
        raise Exception(check + ". Influence cannot be added")

    sim.Add_Land_Influences(pos_1, entity_1_name, characteristic_1_name,
                            pos_2, entity_2_name, characteristic_2_name, c, plus, mult)

def z_deleteInfluence(pos_1, entity_1_name, characteristic_1_name,
                      pos_2, entity_2_name, characteristic_2_name):
    check = Check_Valid_Positions(pos_1[0], pos_1[1])
    if check != None:
        raise Exception(check + ". Influence cannot be deleted")
    check = Check_Valid_Positions(pos_2[0], pos_2[1])
    if check != None:
        raise Exception(check + ". Influence cannot be deleted")

    sim.Delete_Land_Influences(pos_1, entity_1_name, characteristic_1_name,
                               pos_2, entity_2_name, characteristic_2_name)
    
def z_getLenght(list):
    return len(list)