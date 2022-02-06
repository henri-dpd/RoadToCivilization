import os
from Compilacion.grammar import build_grammar
from Compilacion.parse.LR_1 import LR1Parser
from Compilacion.lexer import MyLexer
from cmp.evaluation import evaluate_reverse_parse
from cmp.semantic import Context
from Compilacion.semantic.type_collector import TypeCollector
from Compilacion.semantic.type_builder import TypeBuilder
from Compilacion.semantic.type_checker import TypeChecker
from execute import Execute
from runner import *

code = ''
path =  os.getcwd() + '/plantillas'

file_name = "plantilla8.txt"

with open(path + '/' + file_name, "r") as file:
    code = file.read()

if not code:
    print('No hay codigo que leer')
else:

    G = build_grammar()

    lexer = MyLexer()
    tokens = lexer(code)

    if lexer.errors:
        code_with_lines = ''
        print('Su codigo:')
        for i,line in enumerate(code.split('\n')):
            code_with_lines += f'{i+1}:  {line}\n'
        print(code_with_lines)

        for error in lexer.errors:
            print(error)
    else:

        parser = LR1Parser(G)

        derivation, operations = parser(tokens)


        if parser.error:
            code_with_lines = ''
            print('Su codigo:')
            for i,line in enumerate(code.split('\n')):
                code_with_lines += f'{i+1}:  {line}\n'
            print(code_with_lines)

            print(parser.error)
        else:

            ast = evaluate_reverse_parse(G, derivation, operations, tokens)

            context = Context()

            collector = TypeCollector(context)
            collector.visit(ast)

            builder = TypeBuilder(context)
            builder.visit(ast)

            checker = TypeChecker(context)
            scope = checker.visit(ast)
            
            
            if not (collector.error or builder.error or checker.error):
                print('Programa culmino sin errores:')
                ex = Execute(context)
                program = ex.visit(ast)
                print(program)
                exec(program)
                """
                try:
                    exec(program)
                except Exception as error:
                    print(repr(error))
                """
                

            else:
                
                print('Semantic Errors:')
                print(code)
                for error in checker.errors:
                    print(error)
                for error in builder.errors:
                    print(error)
                    
