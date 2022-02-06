import cmp.visitor as visitor
from Compilacion.astree.AST_Nodes import ast_nodes as nodes
from cmp.semantic import Scope


class Execute:
    def __init__(self, context):
        self.current_type = None
        self.current_method = None
        self.context = context
        self.declared_var =[]
        self.used_var =[]
        self.used_funct =[]
        self.declared_funct =["_start", "_random","_redimention",
                              "_end","_write","_day","_distribution",
                              "_plus","_multiplication","_addLand",
                              "_addSociety","_addSpecies","_deleteLand",
                              "_deleteSociety", "_deleteSpecies","_addDependence",
                              "_deleteDependence","_addInfluence","_deleteInfluence",
                              "_changeCharacteristic","_deleteCharacteristic",
                              "_getCharacteristic","_getCharacteristicSummation",
                              "_getCharacteristicMean","_getLenght","_numberToString",
                              "_booleanToString","_listToString", "_addSociety",
                              "_actualDay", "_enableEvolution"]

    @visitor.on('node')
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.ProgramNode)
    def visit(self, node, scope = None, ident=0):
        scope = Scope() if scope == None else scope

        self.current_type = self.context.get_type("Simulation")
        self.current_method = self.current_type.get_method("_main")
        
        main = ""

        for dec in node.declarations:
            main += "\n" + self.visit(dec, scope, ident)
        
        return main


    @visitor.when(nodes.FuncDeclaration)
    def visit(self, node, scope, ident):
        self.declared_funct.append(node.name)

        self.current_method = self.current_type.get_method(node.name)
        
        params = ""
        for name, typex in zip(self.current_method.param_names, self.current_method.param_types):
            params += "z" + name + ", "
            scope.define_variable(name, self.context.get_type(typex.name))
        
        count_declared_var = len(self.declared_var) - 1
        count_declared_funct = len(self.declared_funct) -1 
        count_used_var = len(self.used_var) - 1
        count_used_funct = len(self.used_funct) -1

        scope.define_variable('self', self.current_type)

        last_line = None
        lines = ""
        for line in node.body:
            lines += "\n" + "\t"*(ident+1) + " " + self.visit(line, scope, ident+1)
            last_line = line
        
        funct = "def " + "z" + node.name + "( "
        duplicate =[]
        for i in self.declared_var[:count_declared_var + 1]:    
            if i in duplicate:
                continue
            duplicate.append(i)
            params += "z" + i + " = " + "z" + i + ", " if i in self.used_var[count_used_var+1:] else ""
        for i in self.declared_funct[:count_declared_funct +1]:    
            if i in duplicate:
                continue
            duplicate.append(i)
            params += "z" + i + " = " + "z" + i + ", " if i in self.used_funct[count_used_funct+1:] and i != node.name else ""
        self.declared_var = self.declared_var[:count_declared_var + 1]
        self.declared_funct = self.declared_var[:count_declared_funct + 1]
        if self.current_method.param_names != [] and count_declared_var == len(self.declared_var) and count_declared_funct == len(self.declared_funct):
                funct += "):"
        funct += params[:-2] + "):"

        funct += lines + "\n" + "\t"*(ident+1) + " return " + "z" + last_line.var
        #funct += lines + "\n" + "\t"*(ident+1) + " print("+ "z" + last_line.var + ")" + "\n" + "\t"*(ident+1) + " return " + "z" + last_line.var

        return funct + "\n"


    @visitor.when(nodes.DeclarationVar)
    def visit(self, node, scope, ident):
        self.declared_var.append(node.var)

        var_type = self.context.get_type(node.type)

        decl = "z" + node.var + " = " + self.visit(node.arith_expr, scope.create_child(), ident+1)
        
        scope.define_variable(node.var, var_type)

        return decl


    @visitor.when(nodes.DeclarationEntity)
    def visit(self, node, scope, ident):
        self.declared_var.append(node.var)

        var_type = self.context.get_type(node.entity)

        decl = "z" + node.var + " = " + node.entity + "( " 
        for arg in node.arg_list:
            param = self.visit(arg, scope, ident+1) + ", "
            decl += param
        if node.arg_list != []:
                decl = decl[:-2]
        decl += ")"
        
        scope.define_variable(node.var, var_type)

        return decl


    @visitor.when(nodes.AsignationVar)
    def visit(self, node, scope, ident):
        self.used_var.append(node.var)

        decl = "z" + node.var + " = " + self.visit(node.arith_expr, scope.create_child(), ident+1)

        return decl


    @visitor.when(nodes.InstanceFunction)
    def visit(self, node, scope, ident):
        self.used_funct.append(node.name)
        if(node.obj == None): 
            inst = "z" + node.name + "( " 
            for arg in node.arg_list:
                if isinstance(arg, nodes.Not) or isinstance(arg, nodes.And) or isinstance(arg, nodes.Or) or isinstance(arg, nodes.LessThan) or isinstance(arg, nodes.MoreThan) or isinstance(arg, nodes.EqualEqual) or isinstance(arg, nodes.BooleanNode):
                    
                    count_declared_var = len(self.declared_var) - 1
                    count_declared_funct = len(self.declared_funct) -1 
                    count_used_var = len(self.used_var) - 1
                    count_used_funct = len(self.used_funct) - 1
                    
                    cond = self.visit(arg, scope, ident+1) + ", "
                    
                    listargs = ""
                    duplicate =[]
                    for i in self.declared_var[:count_declared_var + 1]:    
                        if i in duplicate:
                            continue
                        duplicate.append(i)
                        listargs += "z" + i + " = " + "z" + i  + ", " if i in self.used_var[count_used_var+1:] else ""
                    duplicate =[]
                    for i in self.declared_funct[:count_declared_funct +1]:    
                        if i in duplicate:
                            continue
                        duplicate.append(i)
                        listargs += "z" + i + " = " + "z" + i + ", " if i in self.used_funct[count_used_funct+1:] and i != node.name else ""
                    self.declared_var = self.declared_var[:count_declared_var + 1]
                    self.declared_funct = self.declared_var[:count_declared_funct + 1]
                    if listargs != "":
                        listargs = listargs[:-2]
                    
                    inst += "lambda " + listargs + ": " + cond
                else:
                    inst += self.visit(arg, scope, ident+1) + ", "
            if node.arg_list != []:
                inst = inst[:-2]
            inst += ")"
        else:
            inst = self.visit(node.obj, scope, ident) + "." + "z" + node.name + "( " 
            for arg in node.arg_list:
                inst += self.visit(arg, scope, ident+1) + ", "
            if node.arg_list != []:
                inst = inst[:-2]
            inst += ")"

        return inst
       

    @visitor.when(nodes.IfElse)
    def visit(self, node, scope, ident):

        ifr = "if " + self.visit(node.ifcond, scope, ident+1) + ":"
        for line in node.body:
            ifr += "\n" + "\t"*(ident+1) + " " + self.visit(line, scope.create_child(), ident+1)
        if ifr == "if " + self.visit(node.ifcond,scope, ident+1) + ":":
            ifr += "\n" + "\t"*(ident+1) + " pass"
        elser = "\n" + "\t"*(ident) + " else: "
        for line in node.elseblock:
            elser += "\n" + "\t"*(ident+1) + " " + self.visit(line, scope.create_child(), ident+1)
        if elser != "\n" + "\t"*(ident) + " else: ":
            ifr += elser
        return ifr
        

    @visitor.when(nodes.WhileNode)
    def visit(self, node, scope, ident):

        whiler = "while ( " + self.visit(node.cond, scope, ident) + "):"
        for line in node.body:
            whiler += "\n" + "\t"*(ident+1) + " " + self.visit(line, scope.create_child(), ident+1)
        return whiler

    
    @visitor.when(nodes.Not)
    def visit(self, node, scope, ident):
        nott = "not " + self.visit(node.cond, scope, ident+1) 
        return nott
        
 
    @visitor.when(nodes.NumberNode)
    def visit(self, node, scope, ident):
        return node.exp


    @visitor.when(nodes.BooleanNode)
    def visit(self, node, scope, ident):
        if node.exp == "true": 
            return "True"
        else:
            return "False"


    @visitor.when(nodes.FunctionName)
    def visit(self, node, scope, ident):
        self.used_var.append(node.exp)
        return "z" + node.exp

    @visitor.when(nodes.StringNode)
    def visit(self, node, scope, ident):
        return node.exp


    @visitor.when(nodes.VariableNode)
    def visit(self, node, scope, ident):
        self.used_var.append(node.exp)
        return "z" + node.exp


    @visitor.when(nodes.IndexListNode)
    def visit(self, node, scope, ident):
        ind = self.visit(node.var, scope, ident) + "[" + self.visit(node.index, scope, ident) + "]"
        return ind


    @visitor.when(nodes.ListNode)
    def visit(self, node, scope, ident):
        listt = "["
        for arg in node.arg_list:
            listt += self.visit(arg, scope, ident+1) + ", "
        if node.arg_list != []:
            listt = listt[:-2]
        listt += "]"
        return listt

    
    @visitor.when(nodes.PlusNode)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " + " + self.visit(node.right, scope, ident+1)
        

    @visitor.when(nodes.MinusNode)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " - " + self.visit(node.right, scope, ident+1)

    
    @visitor.when(nodes.StarNode)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " * " + self.visit(node.right, scope, ident+1)


    @visitor.when(nodes.DivNode)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " / " + self.visit(node.right, scope, ident+1)
    

    @visitor.when(nodes.LessThan)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " < " + self.visit(node.right, scope, ident+1)
    
    
    @visitor.when(nodes.MoreThan)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " > " + self.visit(node.right, scope, ident+1)

    
    @visitor.when(nodes.EqualEqual)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " == " + self.visit(node.right, scope, ident+1)
 

    @visitor.when(nodes.And)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " and " + self.visit(node.right, scope, ident+1)


    @visitor.when(nodes.Or)
    def visit(self, node, scope, ident):
        return self.visit(node.left, scope, ident+1)  + " or " + self.visit(node.right, scope, ident+1)