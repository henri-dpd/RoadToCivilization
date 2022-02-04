class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
        self.error = ''
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        operations = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])
            
            try:
                action, tag = self.action[(state, self.G[lookahead.token_type])]
                if action == self.SHIFT:
                    operations.append(self.SHIFT)
                    stack.append(tag)
                    cursor += 1

                elif action == self.REDUCE:
                    operations.append(self.REDUCE)
                    output.append(tag)
                    for _ in tag.Right: stack.pop()
                    a = self.goto[stack[-1],tag.Left]
                    stack.append(a)


                elif action == self.OK:
                    return output,operations
                else:
                    raise NameError
            except:
                self.error = f'Syntax error at line {lookahead.line}'
                return None, None
            
    