from Compilacion.parse.shift_reduce_parser import ShiftReduceParser
from cmp.automata import State, multiline_formatter
from cmp.utils import ContainerSet
from cmp.pycompiler import Item
from Compilacion.parse.auxiliar import compute_firsts, closure_lr1, goto_lr1


def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
            kernels = goto_lr1(current_state.state, symbol, just_kernel=True)
            
            if not kernels:
                continue
            
            try:
                next_state = visited[kernels]
            except KeyError:
                pending.append(kernels)
                visited[pending[-1]] = next_state = State(frozenset(goto_lr1(current_state.state, symbol, firsts)), True)
            
            current_state.add_transition(symbol.Name, next_state)
    
    automaton.set_formatter(multiline_formatter)
    return automaton


class LR1Parser(ShiftReduceParser):
    
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == G.startSymbol:
                        LR1Parser._register(self.action, (idx, G.EOF), (ShiftReduceParser.OK, None))
                    else:
                        for lookahead in item.lookaheads:
                            LR1Parser._register(self.action, (idx, lookahead), (ShiftReduceParser.REDUCE, prod))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        LR1Parser._register(self.action, (idx, next_symbol), (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        LR1Parser._register(self.goto, (idx, next_symbol), node[next_symbol.Name][0].idx)
                pass
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value