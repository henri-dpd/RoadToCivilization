from re import S
import cmp.visitor as visitor
from Compilacion.astree.AST_Nodes import ast_nodes as nodes
from cmp.semantic import SemanticError, Scope, TypeCompatible


WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation "%s" is not defined between "%s" and "%s".'
INVALID_RETURN = 'Return value is not an asignation".'
INVALID_PARAMS = 'Invalid params'
INVALID_NAME = "Inavlid name %s"


class TypeChecker:
    def __init__(self, context):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.error = False
        self.errors = []

    @visitor.on('node')
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.ProgramNode)
    def visit(self, node, scope=None):
        if(self.error):
            return
            
        scope = Scope() if scope == None else scope

        self.current_type = self.context.get_type("Simulation")
        self.current_method = self.current_type.get_method("_main")
        
        for dec in node.declarations:
            self.visit(dec, scope)
            if(self.error):
                return
        
        return scope

    @visitor.when(nodes.FuncDeclaration)
    def visit(self, node, scope):
        if(self.error):
            return
        self.current_method = self.current_type.get_method(node.name)

        scope.define_variable('self', self.current_type)
        scope = scope.create_child()

        if (node.name == "_main" or node.name == "_start" or node.name == "_random" 
            or node.name == "_redimention" or node.name == "_end" or node.name == "_write" 
            or node.name == "_day" or node.name == "_distribution" or node.name == "_plus" 
            or node.name == "_multiplication" or node.name == "_addLand" or node.name == "_addSociety" 
            or node.name == "_addSpecies" or node.name == "_deleteLand" or node.name == "_deleteSociety" 
            or node.name == "_deleteSpecies" or node.name == "_addDependence" or node.name == "_deleteDependence"
            or node.name == "_deleteInfluence" or node.name == "_addInfluence" or node.name == "_changeCharacteristic"
            or node.name == "_deleteCharacteristic" or node.name == "_getCharacteristic" or node.name == "_getCharacteristicSummation"
            or node.name == "_getCharacteristicMean" or node.name == "_getLenght" or node.name == "_numberToString" 
            or node.name == "_booleanToString" or node.name == "_listToString"):
            self.errors.append(INVALID_NAME % (node.name))
            self.error = True
            return TypeCompatible()

        for name, typex in zip(self.current_method.param_names, self.current_method.param_types):
            if scope.is_local(name):
                self.errors.append(LOCAL_ALREADY_DEFINED % (name,self.current_method.name))
                self.error = True
                return TypeCompatible()
        
            elif typex == 'Simulation':
                self.errors.append('Simulation cannot be used as a parameter type')
                self.error = True
                return TypeCompatible()

            else:
                scope.define_variable(name, self.context.get_type(typex.name))
        
        last_line = None
        #body_type = self.visit(node.body, scope)
        for line in node.body:
            if(self.error):
                return
            body_type = self.visit(line, scope)
            if(self.error):
                return
            last_line = line
        
        if node.type in self.context.types:
            returnType = self.context.get_type(node.type)
        
        if not isinstance(last_line, nodes.AsignationVar):
            self.errors.append(INVALID_RETURN)
            self.error = True
            return TypeCompatible()
            
        if not body_type.conforms_to(returnType):
            self.errors.append(INCOMPATIBLE_TYPES % (body_type.name, returnType))
            self.error = True
            return TypeCompatible()
            

        return

    @visitor.when(nodes.DeclarationVar)
    def visit(self, node, scope):
        if(self.error):
            return
        
        var_type = self.context.get_type(node.type)

        type_expr = self.visit(node.arith_expr, scope.create_child())
        if(self.error):
            return

        if not type_expr.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES % (type_expr.name, var_type.name))
            self.error = True
            return TypeCompatible()
                

        scope.define_variable(node.var, var_type)

        return 

    @visitor.when(nodes.DeclarationEntity)
    def visit(self, node, scope):
        if(self.error):
            return
        var_type = self.context.get_type(node.entity)
        var_type2 = self.context.get_type(node.entity2)

        if var_type != var_type2:
            self.errors.append(INCOMPATIBLE_TYPES % (var_type.name, var_type2.name))
            self.error = True
            return TypeCompatible()

        if var_type.name == "Land":
            arg =[]
            for i in node.arg_list:
                arg.append(self.visit(i, scope))
                if(self.error):
                    return
            if len(arg) != 1 or arg[0].name != "List":
                self.errors.append(INVALID_PARAMS)
                self.error = True
                return TypeCompatible()

        if var_type.name == "Species":
            arg =[]
            for i in node.arg_list:
                arg.append(self.visit(i, scope))
                if(self.error):
                    return
            if len(arg) != 1 or arg[0].name != "String":
                self.errors.append(INVALID_PARAMS)
                self.error = True
                return TypeCompatible()

        if var_type.name == "Society":
            arg =[]
            for i in node.arg_list:
                arg.append(self.visit(i, scope))
                if(self.error):
                    return
            if not(((len(arg) == 2  or (len(arg) == 3 and arg[2].name == "List")) 
                     and arg[0].name == "String" and arg[1].name == "Species")):
                self.errors.append(INVALID_PARAMS)
                self.error = True
                return TypeCompatible()
            

        scope.define_variable(node.var, var_type)

        return 
    

    @visitor.when(nodes.AsignationVar)
    def visit(self, node, scope):
        if(self.error):
            return
        var = scope.find_variable(node.var)

        type_expr = self.visit(node.arith_expr, scope.create_child())
        if(self.error):
            return

        if var is None:
            self.errors.append(VARIABLE_NOT_DEFINED % (node.var, self.current_method.name))
            self.error = True
            return TypeCompatible()

        elif not type_expr.conforms_to(var.type):
            self.errors.append(INCOMPATIBLE_TYPES % (type_expr.name, var.type.name))
            self.error = True
            return TypeCompatible()
            

        return type_expr


    @visitor.when(nodes.InstanceFunction)
    def visit(self, node, scope):
        if(self.error):
            return
        if node.obj is None:
            obj_type = self.current_type
        else:
            obj_type = self.visit(node.obj, scope)
            if(self.error):
                return
        
        
        try:
            meth = obj_type.get_method(node.name)
        except SemanticError as se:
            self.errors.append(se.text)
            self.error = True
            return TypeCompatible()
            
        
        if len(node.arg_list) != len(meth.param_names):
            self.errors.append(f'Method {meth.name} defined in {obj_type.name} receive {len(meth.param_names)} parameters')
            self.error = True
            return TypeCompatible()

        for i,arg in enumerate(node.arg_list):
            type_arg = self.visit(arg, scope)
            if(self.error):
                return
            if i < len(meth.param_types) and not type_arg.conforms_to(meth.param_types[i]):
                self.errors.append(INCOMPATIBLE_TYPES % (type_arg.name, meth.param_types[i].name))
                self.error = True
                return TypeCompatible()
        
        return meth.return_type


    @visitor.when(nodes.IfElse)
    def visit(self, node, scope):
        if(self.error):
            return
        if_type = self.visit(node.ifcond, scope.create_child())
        if(self.error):
            return

        if not if_type.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(INCOMPATIBLE_TYPES % (if_type.name, 'Boolean'))
            self.error = True
            return TypeCompatible()

        else_type = []
        body_type = []
        for line in node.body:
            body_type = self.visit(line, scope.create_child())
            if(self.error):
                return
        for line in node.elseblock:
            else_type = self.visit(line, scope.create_child())
            if(self.error):
                return
        if else_type == []:
            return body_type
        return body_type.join(else_type)

    @visitor.when(nodes.WhileNode)
    def visit(self, node, scope):
        if(self.error):
            return
        type_conditional = self.visit(node.cond, scope)
        if(self.error):
            return

        if not type_conditional.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(INCOMPATIBLE_TYPES % (type_conditional.name, 'Boolean'))
            self.error = True
            return TypeCompatible()
        
        #body_type = self.visit(node.body, scope.create_child())
        for line in node.body:
            body_type = self.visit(line, scope.create_child())
            if(self.error):
                return
            
        return body_type
    
    
    @visitor.when(nodes.Not)
    def visit(self, node, scope):
        if(self.error):
            return
        typex = self.visit(node.cond, scope)
        if(self.error):
            return

        if not typex.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(INCOMPATIBLE_TYPES % (typex.name, 'Boolean'))
            self.error = True
            return TypeCompatible()

        return typex

    
    @visitor.when(nodes.NumberNode)
    def visit(self, node, scope):
        if(self.error):
            return
        return self.context.get_type('Number')

    
    @visitor.when(nodes.BooleanNode)
    def visit(self, node, scope):
        if(self.error):
            return
        return self.context.get_type('Boolean')


    @visitor.when(nodes.StringNode)
    def visit(self, node, scope):
        if(self.error):
            return
        return self.context.get_type('String')

    @visitor.when(nodes.FunctionName)
    def visit(self, node, scope):
        if(self.error):
            return

        obj_type = self.current_type
        try:
            meth = obj_type.get_method(node.exp)
        except SemanticError as se:
            self.errors.append(se.text)
            self.error = True
            return TypeCompatible()

        return meth.return_type


    @visitor.when(nodes.VariableNode)
    def visit(self, node, scope):
        if(self.error):
            return
        var = scope.find_variable(node.exp)

        if var is None:
            self.errors.append(VARIABLE_NOT_DEFINED % (node.exp, self.current_method.name))
            self.error = True
            return TypeCompatible()

        return var.type

    
    @visitor.when(nodes.IndexListNode)
    def visit(self, node, scope):
        if(self.error):
            return
        var = scope.find_variable(node.var.exp)

        if var is None:
            self.errors.append(VARIABLE_NOT_DEFINED % (node.var, self.current_method.name))
            self.error = True
            return TypeCompatible()

        if var.type != self.context.get_type('List'):
            self.errors.append(INCOMPATIBLE_TYPES % (var.type, self.context.get_type('List'))) 
            self.error = True
            return TypeCompatible()
        
        type_index = self.visit(node.index,scope)
        if(self.error):
            return
        
        if type_index != self.context.get_type('Number'):
            self.errors.append(INCOMPATIBLE_TYPES % (type_index, self.context.get_type('Number')))
            self.error = True
            return TypeCompatible()

        return TypeCompatible()

    @visitor.when(nodes.ListNode)
    def visit(self, node, scope):
        if(self.error):
            return
        type_arg = None
        for arg in node.arg_list:
            actual_type = self.visit(arg, scope)
            if(self.error):
                return
            if type_arg == None:
                type_arg = self.visit(arg, scope)
                if(self.error):
                    return
                continue
            elif type_arg != actual_type:
                self.errors.append(INCOMPATIBLE_TYPES % (type_arg, actual_type))
                self.error = True
                return TypeCompatible()

            type_arg = actual_type

        return self.context.get_type('List')

    
    @visitor.when(nodes.PlusNode)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left == type_right:
            self.errors.append(INVALID_OPERATION % ('+', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()
            

        else:
            return type_right
    

    @visitor.when(nodes.MinusNode)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Number')) or not type_right.conforms_to(self.context.get_type('Number')):
            self.errors.append(INVALID_OPERATION % ('-', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Number')

    
    @visitor.when(nodes.StarNode)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Number')) or not type_right.conforms_to(self.context.get_type('Number')):
            self.errors.append(INVALID_OPERATION % ('*', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Number')


    @visitor.when(nodes.DivNode)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Number')) or not type_right.conforms_to(self.context.get_type('Number')):
            self.errors.append(INVALID_OPERATION % ('/', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Number')
    

    @visitor.when(nodes.LessThan)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Number')) or not type_right.conforms_to(self.context.get_type('Number')):
            self.errors.append(INVALID_OPERATION % ('<', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Boolean')
    
    @visitor.when(nodes.MoreThan)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Number')) or not type_right.conforms_to(self.context.get_type('Number')):
            self.errors.append(INVALID_OPERATION % ('>', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Boolean')

    
    @visitor.when(nodes.EqualEqual)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return
        
        int_type = self.context.get_type('Number')
        bool_type = self.context.get_type('Boolean')
        string_type = self.context.get_type('String')
        list_type = self.context.get_type('List')
        
        if (type_left == int_type and not type_right.conforms_to(int_type)) or (type_right == int_type and not type_left.conforms_to(int_type)) or (type_left == bool_type and not type_right.conforms_to(bool_type)) or (type_right == bool_type and not type_left.conforms_to(bool_type)) or (type_left == string_type and not type_right.conforms_to(string_type)) or (type_right == string_type and not type_left.conforms_to(string_type)) or (type_left == list_type and not type_right.conforms_to(list_type)) or (type_right == list_type and not type_left.conforms_to(list_type)):
            self.errors.append(INVALID_OPERATION % ('==', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        return bool_type
 
    @visitor.when(nodes.And)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Boolean')) or not type_right.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(INVALID_OPERATION % ('and', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Boolean')

     
    @visitor.when(nodes.Or)
    def visit(self, node, scope):
        if(self.error):
            return
        type_left = self.visit(node.left, scope)
        if(self.error):
            return
        type_right = self.visit(node.right, scope)
        if(self.error):
            return

        if not type_left.conforms_to(self.context.get_type('Boolean')) or not type_right.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(INVALID_OPERATION % ('or', type_left.name, type_right.name))
            self.error = True
            return TypeCompatible()

        else:
            return self.context.get_type('Boolean')

    
