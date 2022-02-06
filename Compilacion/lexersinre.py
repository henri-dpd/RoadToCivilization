from cmp.regex import Regex
from cmp.utils import Token
from cmp.automata import State

'''
Recibe como parametros el lexema, tipo y linea donde se encuentra
'''
class Token:
 
    def __init__(self, lex, ttype): 
        
        self.lex = lex 
        self.token_type = ttype
 
    def __str__(self): 
        return f'{self.ttype}: {self.lex}'
 
'''
El lexer es el resultado de la union de todas las expresiones regulares que forman
el lenguaje
'''


class Lexer:
    def __init__(self, table, ignored_tokens, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
        self.ignored_tokens = ignored_tokens
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            
            
            a,states = State.from_nfa(Regex(regex).automaton,get_states=True)
            for state in states:
                if state.final:
                    state.tag = (n,token_type)
            regexs.append(a)
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        for state in self.regexs:
            start.add_epsilon_transition(state)
        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        lex = ''
        
        for symbol in string:
            # Your code here!!!
            if state.has_transition(symbol):
                lex += symbol
                state = state[symbol][0]
                
                if state.final:
                    final = state
                    final.lex = lex
            else:
                break
        
        if final:
            return final, final.lex
        
        return None, None
    
    def _tokenize(self, text):
        while len(text)>0:
            if text == 0:
                break
            state_final,final = self._walk(text)
            min_tag = 10000
            for state in state_final.state:
                if state.final:
                    n,token_type = state.tag
                    if n < min_tag:
                        min_tag = n
                        final_type = token_type

            text = text[len(final):]
            yield final,final_type
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) if ttype not in self.ignored_tokens]
 
    

'''
Esta clase guardara las propiedades sintacticas de mi lenguaje
'''
nonzero_digits = '|'.join(str(n) for n in range(0,10))
lower_letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
upper_letters = '|'.join(chr(n) for n in range (ord('A'),ord('Z')+1))
letters = lower_letters +'|'+ upper_letters + '|' + '_'
letters_with_space = lower_letters +'|'+ upper_letters + '|' + '_' + '|' + ' '

regexs = [
('while'     ,'while'                      ), 
('false'     ,'false'                      ), 
('else'      ,'else'                       ), 
('true'      ,'true'                       ),
('not'       ,'not'                        ),
('or'        ,'or'                         ), 
('and'       ,'and'                        ),
('{'        ,'\{'                         ),
('}'        ,'\}'                         ),
('('        ,'\('                         ),
(')'        ,'\)'                         ),
('['        ,'\['                         ),
(']'        ,'\]'                         ),
('\.'        ,'\.'                         ), 
('if'        ,'if'                         ),  
('+'        ,'\+'                         ), 
('-'        ,'\-'                         ), 
('*'        ,'\*'                         ),
(','         ,','                          ),
(';'         ,';'                          ),
('/'         ,'/'                          ), 
('<'         ,'<'                          ), 
('>'         ,'>'                          ), 
('='         ,'='                          ),
('=='        ,'=='                         ),
('space'     , '  *'),
('line'      , '\n'),
('var'       ,f'({lower_letters})(0|{letters}|0|{nonzero_digits})*'       ),
('type'      ,f'({upper_letters})({letters}|0|{nonzero_digits})*'       ),
('funct_name',f'_({letters})({letters}|0|{nonzero_digits})*'             ),
('string'    ,'\"'                         ),
('number'    , f'({nonzero_digits})(0|{nonzero_digits})*'                     ),]
        
ignored_tokens = ['space', 'line']
lexer = Lexer(regexs,ignored_tokens,'$')