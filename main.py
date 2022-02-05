
'''from pathlib import Path
from sys import path, set_coroutine_origin_tracking_depth

path.append(str(Path(__file__).parent.parent.absolute()))'''

import os
import streamlit as st
from Compilacion.grammar import build_grammar
from Compilacion.lexer import MyLexer
from Compilacion.parse.LR_1 import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from cmp.semantic import Context
from Compilacion.semantic.type_collector import TypeCollector
from Compilacion.semantic.type_builder import TypeBuilder
from Compilacion.semantic.type_checker import TypeChecker
from execute import Execute
from runner import execute



files = lambda path: [file for file in os.listdir(path) if file[-3:] == '.cl' or file[-4:] == '.txt']


st.title('Road To Civilization')
st.write('Airelys Collazo Perez')
st.write('Henri Daniel Peña Dequero')
st.write('Alejandro Escobar Giraudy')


code = ''
path = st.text_input('Ingrese ruta de Archivo', value = os.getcwd() + '/plantillas')

file_name = st.empty().selectbox(label = 'Seleccione Archivo', options = ['Ninguno Seleccionado'] + files(path))



if file_name and file_name != 'Ninguno Seleccionado':
    with open(path + '/' + file_name, "r") as file:
        code = file.read()

 
code = st.text_area("Introduzca codigo", value = code)


analize = st.button('Analizar')

if analize:
    if not code:
        st.subheader('Ingrese codigo o seleccione archivo')
    else:

        G = build_grammar()

        lexer = MyLexer()
        tokens = lexer(code)

        if lexer.errors:

            st.subheader('Error de sintaxis:')
            
            for error in lexer.errors:
                st.error(error)

            code_with_lines = ''
            st.subheader('Su codigo:')
            for i,line in enumerate(code.split('\n')):
                code_with_lines += f'{i+1}:  {line}\n'
            st.text(code_with_lines)

        else:

            parser = LR1Parser(G)

            derivation, operations = parser(tokens)

            if parser.error:
                code_with_lines = ''
                st.subheader('Su codigo:')
                for i,line in enumerate(code.split('\n')):
                    code_with_lines += f'{i+1}:  {line}\n'
                st.text(code_with_lines)

                st.error(parser.error)
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
                    st.subheader('Programa culmino sin errores:')
                    ex = Execute(context)
                    program = ex.visit(ast)
                    execute(program)
                    st.text(program)

                else:
                   
                    st.subheader('Error semántico:')
                    for error in checker.errors:
                        st.error(error)
                    for error in builder.errors:
                        st.error(error)
                    st.text(code)
                    
