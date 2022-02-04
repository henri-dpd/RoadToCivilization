import cmp.visitor as visitor
from Compilacion.astree.AST_Nodes import ast_nodes as nodes
from cmp.semantic import SemanticError

class TypeBuilder:
    def __init__(self, context):
        self.context = context
        self.current_type = None
        self.error = False
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(nodes.ProgramNode)
    def visit(self,node):
        if(self.error):
            return
        self.current_type = self.context.get_type("Simulation")
        for dec in node.declarations:
            self.visit(dec)
        return
    

    @visitor.when(nodes.DeclarationVar)
    def visit(self,node):
        if(self.error):
            return
        try:
            attrType = self.context.get_type(node.type)
            self.current_type.define_attribute(node.var, attrType)
        except SemanticError as se:
            self.errors.append(se.text)
            self.error = True
            return 
            
        return
    @visitor.when(nodes.DeclarationEntity)
    def visit(self,node):
        if(self.error):
            return
        try:
            attrType = self.context.get_type(node.entity)
            self.current_type.define_attribute(node.var, attrType)
        except SemanticError as se:
            self.errors.append(se.text)
            self.error = True
            return se
            
        return

    
    @visitor.when(nodes.FuncDeclaration)
    def visit(self,node):
        if(self.error):
            return
        param_names = []
        param_types = []

        for type, name in node.arg_types_list:
            param_names.append(name)

            try:
                param_types.append(self.context.get_type(type))
            except SemanticError as se:
                self.errors.append(se.text)
                self.error = True
                return se

        try:       
            returnType = self.context.get_type(node.type)
        except SemanticError as se:
            self.errors.append(se.text)
            self.error = True
            return se
        
        try:
            self.current_type.define_method(node.name, param_names, param_types, returnType)
        except SemanticError as se:
            self.errors.append(se.text)
            self.error = True
            return se

        return