from cmp.pycompiler import Grammar
from Compilacion.astree.AST_Nodes import ast_nodes

def build_grammar():
    Gram = Grammar()

    #No Terminales
    program = Gram.NonTerminal('<program>', startSymbol=True)
    simulation = Gram.NonTerminal('<simulation>')
    declarationnt, arith_expr, funct, term = Gram.NonTerminals('<declarationnt> <arith_expr> <funct> <term>')
    crudcharnt, ifnt, cond, whilent = Gram.NonTerminals('<crudcharnt> <ifnt> <cond> <whilent>')
    asignationnt, arg_list, type_var = Gram.NonTerminals('<asignationnt> <arg_list> <type_var>')
    arg_types_list, functnt, factor = Gram.NonTerminals('<arg_types_list> <functnt> <factor>')
    elseblock, listnt, block, listindexed = Gram.NonTerminals('<elseblock> <listnt> <block> <listindexed>')

    #Terminales
    open_parenthesis, closed_parenthesis, equal, colon, plus, minus, star, div = Gram.Terminals('( ) = , + - * /')
    semicolon, point, open_bracket, closed_bracket, open_square, closed_square = Gram.Terminals('; . { } [ ]')
    ift, elset, whilet, true, false, string, number = Gram.Terminals('if else while true false string number') 
    entity, var, funct_name, typet = Gram.Terminals('entity var funct_name type')
    arg, lessthan, morethan, equalequal, andt, ort, nott = Gram.Terminals('arg < > == and or not')
    
    

    #Producciones
    program %=  simulation, lambda h,s: ast_nodes.ProgramNode(s[1])

    simulation %= declarationnt + semicolon, lambda h,s: [s[1]]
    simulation %= declarationnt + semicolon + simulation, lambda h,s: [s[1]] + s[3]
    simulation %= asignationnt + semicolon, lambda h,s: [s[1]]
    simulation %= asignationnt + semicolon + simulation, lambda h,s: [s[1]] + s[3]
    simulation %= ifnt, lambda h,s: [s[1]]
    simulation %= ifnt + simulation, lambda h,s: [s[1]] + s[2]
    simulation %= whilent, lambda h,s: [s[1]]
    simulation %= whilent + simulation, lambda h,s: [s[1]] + s[2]
    simulation %= functnt, lambda h,s: [s[1]]
    simulation %= functnt + simulation, lambda h,s: [s[1]] + s[2]
    simulation %= crudcharnt + semicolon, lambda h,s: [s[1]]
    simulation %= crudcharnt + semicolon + simulation, lambda h,s: [s[1]] + s[3]
    simulation %= funct + semicolon, lambda h,s: [s[1]]
    simulation %= funct + semicolon + simulation, lambda h,s: [s[1]] + s[3]

    block %= declarationnt + semicolon + block, lambda h,s: [s[1]] + s[3]
    block %= asignationnt + semicolon + block, lambda h,s: [s[1]] + s[3]
    block %= ifnt + block, lambda h,s: [s[1]] + s[2]
    block %= whilent + block, lambda h,s: [s[1]] + s[2]
    block %= crudcharnt + semicolon + block, lambda h,s: [s[1]] + s[3]
    block %= factor + semicolon + block, lambda h,s: [s[1]] + s[3]
    block %= Gram.Epsilon, lambda h,s: []

    arg_list %= cond, lambda h,s: [s[1]]
    arg_list %= arg_list + colon + cond, lambda h,s: s[1] + [s[3]]
    arg_list %= Gram.Epsilon, lambda h,s:  []


    declarationnt %= typet + var + equal + typet + open_parenthesis + arg_list + closed_parenthesis, lambda h,s: ast_nodes.DeclarationEntity(s[1],s[2],s[4],s[6])
    declarationnt %= typet + var + equal + arith_expr, lambda h,s: ast_nodes.DeclarationVar(s[1],s[2],s[4])  
    
    asignationnt %= var + equal + arith_expr, lambda h,s: ast_nodes.AsignationVar(s[1],s[3])  

    arith_expr %= arith_expr + plus + term, lambda h,s: ast_nodes.PlusNode(s[1],s[3])
    arith_expr %= arith_expr + minus + term, lambda h,s: ast_nodes.MinusNode(s[1],s[3])
    arith_expr %= term, lambda h,s:s[1]

    term %= term + star + factor, lambda h,s: ast_nodes.StarNode(s[1],s[3])
    term %= term + div + factor, lambda h,s: ast_nodes.DivNode(s[1],s[3])
    term %= cond, lambda h,s: s[1]

    factor %= open_parenthesis + arith_expr + closed_parenthesis, lambda h,s: s[2]
    factor %= string, lambda h,s: ast_nodes.StringNode(s[1])
    factor %= number, lambda h,s: ast_nodes.NumberNode(s[1])
    factor %= true, lambda h,s: ast_nodes.BooleanNode(s[1])
    factor %= false, lambda h,s: ast_nodes.BooleanNode(s[1])
    factor %= var, lambda h,s: ast_nodes.VariableNode(s[1])
    factor %= funct, lambda h,s: s[1]
    factor %= listnt, lambda h,s: s[1]
    factor %= listindexed, lambda h,s: s[1]

    listnt %= open_square + arg_list + closed_square, lambda h,s: ast_nodes.ListNode(s[2])
    listindexed %= factor + open_square + factor + closed_square, lambda h,s: ast_nodes.IndexListNode(s[1], s[3])

    
    ifnt %= ift + open_parenthesis + cond +closed_parenthesis + open_bracket + block + closed_bracket + elseblock, lambda h,s: ast_nodes.IfElse(s[3],s[6],s[8])

    elseblock %= elset + open_bracket + block + closed_bracket, lambda h,s: s[3] #ast_nodes.Elseblock(s[3])  
    elseblock %= Gram.Epsilon, lambda h,s: []

    cond %= factor, lambda h,s: s[1] 
    cond %= nott + cond, lambda h,s: ast_nodes.Not(s[2])
    cond %= factor + andt + cond, lambda h,s: ast_nodes.And(s[1],s[3]) 
    cond %= factor + ort + cond, lambda h,s: ast_nodes.Or(s[1],s[3])  
    cond %= factor + lessthan + factor, lambda h,s: ast_nodes.LessThan(s[1],s[3])  
    cond %= factor + morethan + factor, lambda h,s: ast_nodes.MoreThan(s[1],s[3])  
    cond %= factor + equalequal + factor, lambda h,s: ast_nodes.EqualEqual(s[1],s[3])  

    funct %= funct_name + open_parenthesis + arg_list + closed_parenthesis, lambda h,s: ast_nodes.InstanceFunction(s[1],s[3]) 
    funct %= factor + point + funct_name + open_parenthesis + arg_list + closed_parenthesis, lambda h,s: ast_nodes.InstanceFunction(s[3],s[5], s[1]) 


    whilent %= whilet + open_parenthesis + cond +closed_parenthesis + open_bracket + block + closed_bracket, lambda h,s: ast_nodes.WhileNode(s[3],s[6])


    functnt %= typet + funct_name + open_parenthesis + arg_types_list + closed_parenthesis + open_bracket + block + closed_bracket, lambda h,s: ast_nodes.FuncDeclaration(s[1],s[2],s[4],s[7])

    arg_types_list %= type_var, lambda h,s: [s[1]]
    arg_types_list %= arg_types_list + colon + type_var, lambda h,s: s[1] + [s[3]]
    arg_types_list %= Gram.Epsilon, lambda h,s: []
    
    type_var %= typet + var, lambda h,s: [s[1], s[2]]
    type_var %= entity + var, lambda h,s: [s[1], s[2]]

    return Gram
