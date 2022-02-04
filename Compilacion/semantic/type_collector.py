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
        specie_type = self.context.create_type('Species')
        land_type = self.context.create_type('Land')
        society_type = self.context.create_type('Society')
        string_type = self.context.create_type('String')
        boolean_type = self.context.create_type('Boolean')
        number_type = self.context.create_type('Number')
        list_type = self.context.create_type('List')
        simulation = self.context.create_type('Simulation')
        

        simulation.define_method('_main', [], [], boolean_type)
        simulation.define_method('_start', [], [], boolean_type) 
        simulation.define_method('_reset', [], [], boolean_type) 
        simulation.define_method('_random', ['i', 'j'], [string_type, list_type], number_type) 
        simulation.define_method('_redimention', ['i', 'j'], [number_type, number_type], boolean_type)
        simulation.define_method('_end', ['i'], [boolean_type], boolean_type)
        simulation.define_method('_write', ['i'], [string_type], boolean_type)
        simulation.define_method('_record', ['i'], [string_type], boolean_type)
        simulation.define_method('_day', ['i', 'j'], [boolean_type, boolean_type], boolean_type)
        simulation.define_method('_distribution', ['i'], [list_type], number_type)
        simulation.define_method('_plus', ['i', 'j'], [list_type, list_type], list_type)
        simulation.define_method('_multiplication', ['i', 'j'], [list_type, list_type], list_type)
        simulation.define_method('_addLand', ['i', 'j', 'k'], [land_type, number_type,number_type], boolean_type)
        simulation.define_method('_addSociety', ['i', 'j', 'k'], [society_type, number_type,number_type], boolean_type)
        simulation.define_method('_deleteLand', ['i', 'j', 'k'], [land_type, number_type,number_type], boolean_type)
        simulation.define_method('_deleteSociety', ['i', 'j', 'k'], [society_type, number_type,number_type], boolean_type)
        simulation.define_method('_updateLand', ['i', 'j', 'k'], [land_type, number_type,number_type], boolean_type)
        simulation.define_method('_updateSociety', ['i', 'j', 'k'], [society_type, number_type,number_type], boolean_type)
        simulation.define_method('_addDependence', ['pos1', 'entity1_name', 'characteristic1_name','pos2', 'entity2_name', 'characteristic2_name', 'c', 'plus', 'mult'], [list_type, string_type, string_type,list_type, string_type, string_type, list_type, list_type, list_type], boolean_type)
        simulation.define_method('_addInfluence', ['pos1', 'entity1_name', 'charac1teristic1_name','pos2', 'entity2_name', 'characteristic2_name', 'c', 'plus', 'mult'], [list_type, string_type, string_type,list_type, string_type, string_type, list_type, list_type, list_type], boolean_type)
        
        land_type.define_method('_addCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        society_type.define_method('_addCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        specie_type.define_method('_addCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        land_type.define_method('_updateCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        society_type.define_method('_updateCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        specie_type.define_method('_updateCharacteristic', ['name', 'value', 'liminf', 'limsup', 'mutab', 'dist'], [string_type, list_type, number_type, number_type, number_type, number_type], boolean_type)
        land_type.define_method('_deleteCharacteristic', ['name'], [string_type], boolean_type)
        society_type.define_method('_deleteCharacteristic', ['name'], [string_type], boolean_type)
        specie_type.define_method('_deleteCharacteristic', ['name'], [string_type], boolean_type)
 
        
        return
    