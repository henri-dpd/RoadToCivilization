import cmp.visitor as visitor
from Compilacion.astree.AST_Nodes import ast_nodes as nodes

class TypeCollector(object):
    def __init__(self, context):
        self.context = context
        self.error = False
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(nodes.ProgramNode)
    def visit(self, node):

        # añadimos algunos tipos predeterminados
        species_type = self.context.create_type('Species')
        land_type = self.context.create_type('Land')
        society_type = self.context.create_type('Society')
        string_type = self.context.create_type('String')
        boolean_type = self.context.create_type('Boolean')
        number_type = self.context.create_type('Number')
        list_type = self.context.create_type('List')
        simulation = self.context.create_type('Simulation')
        

        simulation.define_method('_main', [], [], boolean_type)
        simulation.define_method('_start', [], [], boolean_type) 
        simulation.define_method('_random', ['i', 'j'], [string_type, list_type], number_type) 
        simulation.define_method('_redimention', ['i', 'j'], [number_type, number_type], boolean_type)
        simulation.define_method('_end', ['i'], [boolean_type], boolean_type)
        simulation.define_method('_write', ['i', 'j'], [string_type, string_type], boolean_type)
        simulation.define_method('_day', ['i', 'j'], [boolean_type, boolean_type], boolean_type)
        simulation.define_method('_distribution', ['i'], [list_type], number_type)
        simulation.define_method('_plus', ['i', 'j'], [list_type, list_type], list_type)
        simulation.define_method('_multiplication', ['i', 'j'], [list_type, list_type], list_type)
        simulation.define_method('_addLand', ['i', 'j', 'k'], [land_type, number_type,number_type], boolean_type)
        simulation.define_method('_addSociety', ['i', 'j', 'k'], [society_type, number_type,number_type], boolean_type)
        simulation.define_method('_addSpecies', ['i'], [species_type], boolean_type)
        simulation.define_method('_deleteLand', ['i', 'j'], [number_type, number_type], boolean_type)
        simulation.define_method('_deleteSociety', ['i', 'j', 'k'], [society_type, number_type,number_type], boolean_type)
        simulation.define_method('_deleteSpecies', ['i'], [species_type], boolean_type)
        simulation.define_method('_addDependence', ['pos_1', 'entity_1_name', 'characteristic_1_name','pos_2', 'entity_2_name', 'characteristic_2_name', 'c', 'plus', 'mult'], [list_type, string_type, string_type,list_type, string_type, string_type, list_type, list_type, list_type], boolean_type)
        simulation.define_method('_addInfluence', ['pos_1', 'entity_1_name', 'charac1teristic_1_name','pos_2', 'entity_2_name', 'characteristic_2_name', 'c', 'plus', 'mult'], [list_type, string_type, string_type,list_type, string_type, string_type, list_type, list_type, list_type], boolean_type)
        simulation.define_method('_deleteDependence', ['pos_1', 'entity_1_name', 'characteristic_1_name','pos_2', 'entity_2_name', 'characteristic_2_name'], [list_type, string_type, string_type,list_type, string_type, string_type], boolean_type)
        simulation.define_method('_deleteInfluence', ['pos_1', 'entity_1_name', 'characteristic_1_name','pos_2', 'entity_2_name', 'characteristic_2_name'], [list_type, string_type, string_type,list_type, string_type, string_type], boolean_type)
        simulation.define_method('_getCharacteristic', ['pos', 'entity', 'name'], [list_type, string_type, string_type], list_type)
        simulation.define_method('_getCharacteristicSummation', ['species','name'], [string_type,string_type], number_type)
        simulation.define_method('_getCharacteristicMean', ['species','name'], [string_type,string_type], number_type)
        simulation.define_method('_getLenght', ['name'], [list_type], number_type)
        simulation.define_method('_numberToString', ['name'], [number_type], string_type)
        simulation.define_method('_booleanToString', ['name'], [boolean_type], string_type)
        simulation.define_method('_listToString', ['name'], [list_type], string_type)
        simulation.define_method('_actualDay', [], [], number_type)
        simulation.define_method('_enableEvolution', ['entity', 'i', 'j'], [string_type, number_type, number_type], boolean_type)
        
        
        land_type.define_method('_addSociety', ['name'], [society_type], boolean_type)
        land_type.define_method('_addDependence', ['entity_1_name', 'characteristic_1_name', 'entity_2_name', 'characteristic_2_name', 'c', 'plus', 'mult'], [ string_type, string_type, string_type, string_type, list_type, list_type, list_type], boolean_type)
        land_type.define_method('_deleteDependence', ['entity_1_name', 'characteristic_1_name', 'entity_2_name', 'characteristic_2_name'], [ string_type, string_type, string_type, string_type], boolean_type)
        land_type.define_method('_addInfluence', ['entity_1_name', 'characteristic_1_name', 'entity_2_name', 'characteristic_2_name', 'c', 'plus', 'mult'], [ string_type, string_type, string_type, string_type, list_type, list_type, list_type], boolean_type)
        land_type.define_method('_deleteInfluence', ['entity_1_name', 'characteristic_1_name', 'entity_2_name', 'characteristic_2_name'], [ string_type, string_type, string_type, string_type], boolean_type)
        land_type.define_method('_changeCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        land_type.define_method('_deleteCharacteristic', ['name'], [string_type], boolean_type)
        society_type.define_method('_changeCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        society_type.define_method('_deleteCharacteristic', ['name'], [string_type], boolean_type)
        species_type.define_method('_changeCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        species_type.define_method('_deleteCharacteristic', ['name'], [string_type], boolean_type)

        
        return
    