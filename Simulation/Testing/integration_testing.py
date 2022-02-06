
from pathlib import Path
from sys import path
import logging

path.append(str(Path(__file__).parent.parent.absolute()))

from simulation import Simulation
from land import Land
from society import Society
from species import Species
from evolution import Evolution
import operators


def evolution_test():
    sim = Simulation(2,2)
    sim.Add_Species("Humano")
    sim.Add_Society(0, 0, "Cubano", "Humano")
    sim.Add_Society(0, 0, "Español", "Humano")
    sim.Add_Society(1, 1,"Americano", "Humano")
    sim.map[0][0].entities["Español"].enable_evolution = False
    sim.map[1][1].entities["Americano"].enable_evolution = False
    sim.Change_Society_Characteristic(0,0, "Español", "Poblacion", 3)
    sim.Change_Society_Characteristic(0,0, "Cubano", "Poblacion", 10)
    sim.Change_Society_Characteristic(0, 0, "Cubano", "Economía", 10)
    sim.Change_Society_Characteristic(0, 0, "Cubano", "Coronavirus", -5)
    sim.Add_Land_Dependences(0, 0 , "Cubano", "Coronavirus", "Cubano", "Poblacion", 1)
    sim.Add_Land_Dependences(0, 0 , "Cubano", "Economía", "Cubano", "Poblacion", 1)
    sim.Add_Land_Dependences(0, 0 , "Español", "Poblacion", "Cubano", "Economía", 1)
    sim.Add_Inter_Dependence([1,1], "Americano", "Poblacion", [0,0], "Cubano", "Poblacion", -1)

    day = 1

    print("Día " + str(day) + ": \n")
    sim.Move_One_Day_All()
    day = day + 1
    print(sim.map[0][0].entities["Cubano"].evolution.society_name)
    print(sim.map[0][0].entities["Cubano"].evolution.pos)
    print(sim.map[0][0].entities["Cubano"].evolution.characteristics)
    print(sim.map[0][0].entities["Cubano"].evolution.inter_dependences)
    print(sim.map[0][0].entities["Cubano"].evolution.values)
    print(sim.map[0][0].entities["Cubano"].evolution.old_values)
    print(sim.map[0][0].entities["Cubano"].evolution.attemps)
    print(sim.map[0][0].entities["Cubano"].evolution.attemp_success)
    print(sim.map[0][0].entities["Cubano"].evolution.request)
    print(sim.map[0][0].entities["Cubano"].evolution.request_pos)
    print("Español: ")
    print(sim.map[0][0].entities["Español"].characteristic["Poblacion"].value)
    print("Americano")
    print(sim.map[1][1].entities["Americano"].characteristic["Poblacion"].value)

    print("Día " + str(day) + ": \n")
    sim.Move_One_Day_All()
    day = day + 1
    print(sim.map[0][0].entities["Cubano"].evolution.society_name)
    print(sim.map[0][0].entities["Cubano"].evolution.pos)
    print(sim.map[0][0].entities["Cubano"].evolution.characteristics)
    print(sim.map[0][0].entities["Cubano"].evolution.inter_dependences)
    print(sim.map[0][0].entities["Cubano"].evolution.values)
    print(sim.map[0][0].entities["Cubano"].evolution.old_values)
    print(sim.map[0][0].entities["Cubano"].evolution.attemps)
    print(sim.map[0][0].entities["Cubano"].evolution.attemp_success)
    print(sim.map[0][0].entities["Cubano"].evolution.request)
    print(sim.map[0][0].entities["Cubano"].evolution.request_pos)
    print("Español: ")
    print(sim.map[0][0].entities["Español"].characteristic["Poblacion"].value)
    print("Americano")
    print(sim.map[1][1].entities["Americano"].characteristic["Poblacion"].value)

    print("Día " + str(day) + ": \n")
    sim.Move_One_Day_All()
    day = day + 1
    print(sim.map[0][0].entities["Cubano"].evolution.society_name)
    print(sim.map[0][0].entities["Cubano"].evolution.pos)
    print(sim.map[0][0].entities["Cubano"].evolution.characteristics)
    print(sim.map[0][0].entities["Cubano"].evolution.inter_dependences)
    print(sim.map[0][0].entities["Cubano"].evolution.values)
    print(sim.map[0][0].entities["Cubano"].evolution.old_values)
    print(sim.map[0][0].entities["Cubano"].evolution.attemps)
    print(sim.map[0][0].entities["Cubano"].evolution.attemp_success)
    print(sim.map[0][0].entities["Cubano"].evolution.request)
    print(sim.map[0][0].entities["Cubano"].evolution.request_pos)
    print("Español: ")
    print(sim.map[0][0].entities["Español"].characteristic["Poblacion"].value)
    print("Americano")
    print(sim.map[1][1].entities["Americano"].characteristic["Poblacion"].value)

    print("Día " + str(day) + ": \n")
    sim.Move_One_Day_All()
    day = day + 1
    print(sim.map[0][0].entities["Cubano"].evolution.society_name)
    print(sim.map[0][0].entities["Cubano"].evolution.pos)
    print(sim.map[0][0].entities["Cubano"].evolution.characteristics)
    print(sim.map[0][0].entities["Cubano"].evolution.inter_dependences)
    print(sim.map[0][0].entities["Cubano"].evolution.values)
    print(sim.map[0][0].entities["Cubano"].evolution.old_values)
    print(sim.map[0][0].entities["Cubano"].evolution.attemps)
    print(sim.map[0][0].entities["Cubano"].evolution.attemp_success)
    print(sim.map[0][0].entities["Cubano"].evolution.request)
    print(sim.map[0][0].entities["Cubano"].evolution.request_pos)
    print("Español: ")
    print(sim.map[0][0].entities["Español"].characteristic["Poblacion"].value)
    print("Americano")
    print(sim.map[1][1].entities["Americano"].characteristic["Poblacion"].value)


    for i in range(10):
        print("Día " + str(day) + ": \n")
        sim.Move_One_Day_All()
        day = day + 1

    print(sim.map[0][0].entities["Cubano"].evolution.society_name)
    print(sim.map[0][0].entities["Cubano"].evolution.pos)
    print(sim.map[0][0].entities["Cubano"].evolution.characteristics)
    print(sim.map[0][0].entities["Cubano"].evolution.inter_dependences)
    print(sim.map[0][0].entities["Cubano"].evolution.values)
    print(sim.map[0][0].entities["Cubano"].evolution.old_values)
    print(sim.map[0][0].entities["Cubano"].evolution.attemps)
    print(sim.map[0][0].entities["Cubano"].evolution.attemp_success)
    print(sim.map[0][0].entities["Cubano"].evolution.request)
    print(sim.map[0][0].entities["Cubano"].evolution.request_pos)

    print("Español: ")
    print(sim.map[0][0].entities["Español"].characteristic["Poblacion"].value)
    print("Americano")
    if("Americano" in sim.map[1][1].entities):
        print(sim.map[1][1].entities["Americano"].characteristic["Poblacion"].value)
    else:
        print("Se murieron los americanos :) wiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")

def society_test():
    humanidad = Species("Humano")
    cuba = Society('Cuba', humanidad)
    print( cuba.name == 'Cuba')
    print( cuba.Get_Characteristic_Value('Poblacion') == 10)
    
    cuba.Set_Default_Characteristics()
    print( len(cuba.characteristic) == 13)
    
    #Testeando caracteristicas
    print( cuba.Get_Characteristic_Value('Poblacion') == 10)
    cuba.Change_Characteristic('Poblacion', 100, 0, 5000)
    print( cuba.Get_Characteristic_Value('Poblacion') == 100)
    
    print( len(cuba.characteristic) == 13)
    cuba.Delete_Characteristic('Crecimiento Actual')
    print( len(cuba.characteristic) == 12)
    print( 'Crecimiento Actual' not in cuba.characteristic)
    cuba.Delete_Characteristic('Crecimiento Actual')
    print( len(cuba.characteristic) == 12)
    
    cuba.Change_Characteristic('politics', 10000)
    print( cuba.Get_Characteristic_Value('politics') == 10000)
    print( len(cuba.characteristic) == 13)
    
    china = Society('China', humanidad)
    print( china.name == 'China')
    print( china.Get_Characteristic_Value('Poblacion') == 10)
    
    china.Set_Default_Characteristics()
    print( len(china.characteristic) == 13    )
    
    china.Change_Characteristic('Poblacion', 220)
    print( china.Get_Characteristic_Value('Poblacion') == 220)



def simulation_test() -> None:
    sim = Simulation(2,3)
    
    #Testeando añadir
    res1 = False
    res2 = False
    sim.Add_Species('Humano')
    sim.Add_Species('Marciano')
    sim.actual_species["Humano"].Set_Default_Characteristics()
    sim.actual_species["Marciano"].Set_Default_Characteristics()  
    for actual in sim.actual_species.values():
        if actual.name == 'Humano':
            res1 = True            
        if actual.name == 'Marciano':
            res2 = True    
    print( res1)
    print( res2    )
    res1 = False
    res2 = False
    res3 = False
    sim.Add_Species('Humano')    
    sim.Add_Species('Yedi')
    sim.actual_species["Yedi"].Set_Default_Characteristics()
    for actual in sim.actual_species.values():
        if actual.name == 'Humano':
            res1 = True            
        if actual.name == 'Marciano':
            res2 = True            
        if actual.name == 'Yedi':
            res3 = True    
    print( res1 )
    print( res2)
    print( res3)
    print( len(sim.actual_species)==3)
    
    #Testeando eliminar
    print( sim.Delete_Species(20) == None)
    print( len(sim.actual_species)==3)
    print( sim.Delete_Species("juan") == None)
    print( len(sim.actual_species)==3)
    
    sim.Delete_Species('Marciano')
    res1 = False
    res2 = False
    res3 = True  
    for actual in sim.actual_species.values():
        if actual.name == 'Humano':
            res1 = True            
        if actual.name == 'Yedi':
            res2 = True    
        if actual.name == 'Marciano':
            res3 = False    
    print( res1 )
    print( res2)
    print( res3)
    print( len(sim.actual_species)==2)

    for specie in sim.actual_species:
        for i in range(sim.rows):
            for j in range(sim.columns):
                sim.Add_Society(i,j,specie, specie)                                
        sim.Set_Default_Species_Characteristic(specie)
        print( len(sim.actual_species[specie].characteristic) == 13)

    for i in range(2):
        for j in range(3):
            sim.Set_Default_Land_Characteristic(i,j)
            print( len(sim.map[i][j].characteristic) == 6)
    
    # Actualmente tenemos tenemos dos especies con las ccaracteristicas por defecto, y un terreno de 2 filas y 3 columnas 
    # A continuación agregaremos 3 interpedendencias especie especie, terreno terreno, terreno especie 
    # Luego comprobaremos que efectivamente la simulación se mueve un día y se cambia de valor las características
    
    sim.Add_Inter_Dependence([1,1], "Humano","Poblacion", [1,1],"Yedi", "Economía",5)
    sim.Move_One_Day_Inter_Dependences()
    print( (sim.map[1][1]).Get_Entities_Characteristic_value('Yedi', "Economía") > 1)
    
    sim.Add_Inter_Dependence([1,2], "","Altitud", [1,1],"", "Temperatura",-1)
    sim.Move_One_Day_Inter_Dependences()
    print( not ((sim.map[1][1]).Get_Entities_Characteristic_value('',"Temperatura") == [0,1]))
    
    
    sim.Add_Inter_Dependence([0,0], "","Capacidad de Recursos", [0,0],"Humano", "Esperanza de Vida",2)
    sim.Move_One_Day_Inter_Dependences()
    print( (sim.map[0][0]).Get_Entities_Characteristic_value('Humano', "Esperanza de Vida") > 1)
    
    #Por último agregaremos dependencias entre especies y correremos todo un día verificando los avances
    sim.Add_Land_Dependences(0,1,"Humano","Poblacion","Humano","Poblacion",2)
    sim.Change_Land_Characteristic(0,1,"Fertilidad",[1,2])
    sim.Add_Land_Dependences(0,1,"","Fertilidad","","Capacidad de Recursos",10)
    
    sim.Move_One_Day_All()
    print( (sim.map[1][1]).Get_Entities_Characteristic_value("Yedi","Economía") == 201)
    print( (sim.map[1][1]).Get_Entities_Characteristic_value("","Temperatura") == [-3,-2])
    print( (sim.map[0][0]).Get_Entities_Characteristic_value("Humano","Esperanza de Vida") == 5)
    print( (sim.map[0][1]).Get_Entities_Characteristic_value("Humano", "Poblacion") == 30)
    print( (sim.map[0][1]).Get_Entities_Characteristic_value("","Capacidad de Recursos") == 11 or (sim.map[0][1]).Get_Entities_Characteristic_value("","resources_capacity") == 21)
    
def land_test() -> None:

     #Creando Land y poniendo caracteristicas por defecto
    terreno = Land([0,0])
    print( terreno.characteristic == {})
    print( terreno.characteristic_dependences == [])
    
    terreno.Set_Default_Characteristics()
    print( len(terreno.characteristic) == 6)
    
    #Testeando caracteristicas
    print( terreno.Get_Characteristic_Value('Recursos Actuales') == 1)
    terreno.Change_Characteristic('Recursos Actuales', 500, 0, 21000)
    print( terreno.Get_Characteristic_Value('Recursos Actuales') == 500)
    
    print( len(terreno.characteristic) == 6)
    terreno.Delete_Characteristic('Recursos Actuales')
    print( len(terreno.characteristic) == 5)
    print( 'Recursos Actuales' not in terreno.characteristic)
    terreno.Delete_Characteristic('Recursos Actuales')
    print( len(terreno.characteristic) == 5)
    
    terreno.Change_Characteristic('Recursos Actuales', 1000)
    print( terreno.Get_Characteristic_Value('Recursos Actuales') == 1000)
    print( len(terreno.characteristic) == 6)
    
    #Testeando dependencias
    terreno.Add_Dependence('','Altitud', '','Temperatura', 1)
    print( len(terreno.characteristic_dependences) == 1)
    terreno.Add_Dependence('','Fertilidad', '','Recursos Actuales', 20)
    print( len(terreno.characteristic_dependences) == 2)
    terreno.Add_Dependence('', 'Fertilidad', '', 'Recursos Actuales', 20)
    print( len(terreno.characteristic_dependences) == 2)
    #orden de las dependencias
    terreno.Add_Dependence('', 'Recursos Actuales','',  'Fertilidad', 10)
    print( len(terreno.characteristic_dependences) == 3)
    terreno.Delete_Dependence('','Altitud', '','Temperatura')
    print( len(terreno.characteristic_dependences) == 2)
    
    terreno.Change_Dependences_Value('','Recursos Actuales','', 'Fertilidad', 0.001)
    print( terreno.characteristic_dependences[1].c == 0.001)
    
    terreno.Delete_Dependence('', 'Altitud', '', 'Temperatura')
    print( len(terreno.characteristic_dependences) == 2)
    
    terreno.Add_Dependence('', 'Recursos Actuales', '', 'Recursos Actuales', 0.005)
    print( len(terreno.characteristic_dependences) == 3)
    print( terreno.characteristic_dependences[2].c == 0.005)
    
    terreno.Add_Influences('','Altitud', '', 'Temperatura', 5)
    terreno.Add_Influences('','Fertilidad','', 'Nivel de Acogimiento', 5)
    print( len(terreno.characteristic_influences) == 2)
    print( terreno.Get_Characteristic_Value('Recursos Actuales') == 1000)
    print( terreno.Move_One_Day() == None)
    print( terreno.Get_Characteristic_Value('Recursos Actuales') > 500)
    for i in range(1000):
        print( terreno.Move_One_Day() == None)
    #Altura no cambia por lo tanto temperatura se mantiene igual aunque este influenciado por la altura
    print( terreno.Get_Characteristic_Value('Temperatura') == [0,1])
    print( terreno.Get_Characteristic_Value('Recursos Actuales') > 20000)
    print( terreno.Get_Characteristic_Value('Fertilidad')[0] > 5000 and terreno.Get_Characteristic_Value('Fertilidad')[1] > 5000)
    #Aqui sin embargo nivel de acogimiento esta influenciado por fertilidad, 
    #como fertilidad cambia significativamente el nivel de acogimiento tambien
    print( terreno.Get_Characteristic_Value('Nivel de Acogimiento') > 40000)
    


    terreno.Add_Society("Cuba", Species("Humanos"))
    terreno.Delete_Society("Cuba")
    terreno.Add_Society("Cuba", Species("Homo-sapiens"))
    
    terreno.Set_Default_Entities_Characteristic("Cuba")
    terreno.Add_Dependence("Cuba", "Poblacion", "Cuba", "Poblacion", 100)
    
    terreno.Add_Dependence("Cuba", "Poblacion", "", "Altitud", 2)
    print( terreno.Get_Characteristic_Value('Altitud') == 1)
    print( terreno.Move_One_Day() == None)
    print( terreno.Get_Entities_Characteristic_value("Cuba","Poblacion") == 1010)
    print( terreno.Get_Characteristic_Value('Altitud') == 21)
    print( terreno.Move_One_Day() == None)
    print( terreno.Get_Entities_Characteristic_value("Cuba","Poblacion") == 102010)
    print( terreno.Get_Characteristic_Value('Altitud') == 2041)

evolution_test()