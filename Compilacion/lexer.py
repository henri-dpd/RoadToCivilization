import re

'''
Recibe como parametros el lexema, tipo y linea donde se encuentra
'''
class Token:
 
    def __init__(self, lex, ttype, line): 
        
        self.lex = lex 
        self.token_type = ttype
        self.line = line
 
    def __str__(self): 
        return f'{self.ttype}: {self.lex}'
 
'''
El lexer es el resultado de la union de todas las expresiones regulares que forman
el lenguaje
'''
class Lexer: 

    def __init__(self, table, keywords, ignored_tokens, eof):
        self.line = 1
        self.table = table
        self.keywords = keywords
        self.ignored_tokens = ignored_tokens
        self.regex = self._build_regex(table)
        self.errors = []
        self.eof = eof
        
 
    def tokenize(self,text):    
        while len(text) > 0:

            match = self.regex.match(text)
            error_token = ''
 
            while not match:
                error_token += text[0]
                text = text[1:]
                if len(text) <= 0: break
                match = self.regex.match(text)

            if error_token:
                self.errors.append(f'Syntax error, unexpexted token "{error_token}" at line {self.line}')
                if len(text) <= 0: continue

            lexeme = match.group()

            if lexeme == '\n':
                self.line += 1


            # STRINGS
            elif lexeme == '"':
                text = text[1:]
                while len(text) > 0:
                    c = text[0]
                    text = text[1:]

                    if c == '\\':
                        if text[0] == 'b':
                            lexeme += '\\b'

                        elif text[0] == 't':
                            lexeme += '\\t'

                        elif text[0] == 'n':
                            lexeme += '\\n'

                        elif text[0] == 'f':
                            lexeme += '\\f'
                        
                        else:
                            lexeme += text[0]

                        text = text[1:]
                    
                    elif c == '\n':
                        self.errors.append(f'Syntax error at line {self.line} : Undefined string')
                        self.line += 1
                        break
                    
                    elif c == '\0':
                        self.errors.append(f'Syntax error at line {self.line} : String cannot contain the null character')
                    
                    else:
                        lexeme += c
                        if c == '"':
                            break
                
                else:
                    self.errors.append(f'Syntax error at line {self.line} : String cannot contain EOF')



            token_type = match.lastgroup if lexeme.lower() not in self.keywords and match.lastgroup is not None else match.group().lower()
 
            yield lexeme, token_type, self.line
 
            text = text[match.end():] if lexeme[0] != '"' else text

        yield '$', self.eof, self.line
 
    def _build_regex(sef,table):
        return re.compile('|'.join([f'(?P<{name}>{regex})' if name != regex else f'({name})' for name,regex in table.items()]))
 
    def __call__(self, text): 
        return [Token(lex, ttype, line) for lex, ttype, line in self.tokenize(text) if ttype not in self.ignored_tokens]

'''
Esta clase guardara las propiedades sintacticas de mi lenguaje
'''
class MyLexer(Lexer):
    def __init__(self):
        self.regexs = {
        'var'       : r'[a-z][a-zA-Z0-9_]*'         ,
        'type'      : r'[A-Z][a-zA-Z0-9_]*'         ,
        'funct_name': r'_[a-zA-Z0-9_]*'         ,
        'string'    : r'\"'                         ,
        'number'    : r'(\(-\d+(\.\d+)?\))|(\d+(\.\d+)?)'                        ,
        'newline'   : r'\n'                         ,
        'whitespace': r' +'                         ,
        'tabulation': r'\t+'                        ,
        'while'     : r'while'                      , 
        'false'     : r'false'                      , 
        'else'      : r'else'                       , 
        'true'      : r'true'                       ,
        'not'       : r'not'                        ,
        'or'        : r'or'                         , 
        'and'       : r'and'                        ,
        '\{'        : r'\{'                         ,
        '\}'        : r'\}'                         ,
        '\('        : r'\('                         ,
        '\)'        : r'\)'                         ,
        '\['        : r'\['                         ,
        '\]'        : r'\]'                         ,
        '\.'        : r'\.'                         , 
        'if'        : r'if'                         ,  
        '\+'        : r'\+'                         , 
        '\-'        : r'\-'                         , 
        '\*'        : r'\*'                         ,
        ','         : r','                          ,
        ';'         : r';'                          ,
        '/'         : r'/'                          , 
        '<'         : r'<'                          , 
        '>'         : r'>'                          , 
        '='         : r'='                          ,
        '=='        : r'=='                         }
               
                   
        self.keywords = ['while','false', 'else', 'not','if','and','or', 'true']
        
        self.ignored_tokens = ['newline','whitespace','tabulation']

        Lexer.__init__(self, self.regexs, self.keywords, self.ignored_tokens, 'eof')