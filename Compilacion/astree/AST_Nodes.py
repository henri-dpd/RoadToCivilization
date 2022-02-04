class ast_nodes:

    class Node:
        pass


    class ProgramNode(Node):
        def __init__(self, declarations):
            self.declarations = declarations


    class DeclarationNode(Node):
        pass
    class ExpressionNode(Node):
        pass
    
    class DeclarationEntity(DeclarationNode):
        def __init__(self, entity, var, entity2, arg_list):
            self.entity = entity
            self.var = var
            self.entity2 = entity2
            self.arg_list = arg_list

    class DeclarationVar(DeclarationNode):
        def __init__(self, type, var, arith_expr):
            self.type = type
            self.var = var
            self.arith_expr = arith_expr

    class FuncDeclaration(DeclarationNode):
        def __init__(self, type, name, arg_types_list, body):
            self.type = type
            self.name = name
            self.arg_types_list = arg_types_list
            self.body = body

    class AsignationVar(ExpressionNode):
        def __init__(self, var, arith_expr):
            self.var = var
            self.arith_expr = arith_expr

    class FactorNode(ExpressionNode):
        def __init__(self, exp):
            self.exp = exp
    
    class BooleanNode(FactorNode):
        pass
    class StringNode(FactorNode):
        pass
    class NumberNode(FactorNode):
        pass
    class VariableNode(FactorNode):
        pass

    class ListNode(ExpressionNode):
        def __init__(self, arg_list):
            self.arg_list = arg_list
    
    class IndexListNode(ExpressionNode):
        def __init__(self, var, index):
            self.var = var
            self.index = index

    class IfElse(ExpressionNode):
        def __init__(self,ifcond,body,elseblock):
            self.ifcond = ifcond
            self.body = body
            self.elseblock = elseblock


    class Not (ExpressionNode):
        def __init__(self, cond):
            self.cond = cond

    class InstanceFunction(ExpressionNode):
        def __init__(self, name, arg_list, obj = None):
            self.obj = obj
            self.name = name
            self.arg_list = arg_list

    class WhileNode (ExpressionNode):
        def __init__(self,cond, body):
            self.cond = cond
            self.body = body

    class BinaryNode(ExpressionNode):
        def __init__(self, left, right):
            self.left = left
            self.right = right

    class And (BinaryNode):
        pass
    class Or (BinaryNode):
        pass
    class LessThan (BinaryNode):
        pass
    class MoreThan (BinaryNode):
        pass
    class EqualEqual (BinaryNode):
        pass


    class PlusNode(BinaryNode):
        pass
    class MinusNode(BinaryNode):
        pass
    class StarNode(BinaryNode):
        pass
    class DivNode(BinaryNode):
        pass