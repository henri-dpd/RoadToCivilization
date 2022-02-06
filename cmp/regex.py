from cmp.ast import AtomicNode,BinaryNode,UnaryNode
from cmp.pycompiler import Grammar
from cmp.tools.automata import(DFA,NFA,automata_closure,automata_concatenation,automata_minimization,automata_union,nfa_to_dfa)
from cmp.tools.evaluation import evaluate_parse
from cmp.tools.parsing import metodo_predictivo_no_recursivo
from cmp.utils import Token

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states=1,finals=[0],transitions={})

class SymbolNode(AtomicNode):
    def evaluate(self):
        s=self.lex
        return DFA(states=2,finals=[1],transitions={(0,s):1})

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue,rvalue):
        return automata_union(lvalue,rvalue)

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue,rvalue):
        return automata_concatenation(lvalue,rvalue)

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    # > fixed_tokens = ???
    fixed_tokens = { lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
    
    literal = False
    
    for char in text:
        if literal:
            tokens.append(Token(char, G['symbol']))
            literal = False
            continue
            
        if skip_whitespaces and char.isspace():
            continue
            
        if char == '\\':
            literal = True
            continue
            
        try:
            tokens.append(fixed_tokens[char])
        except KeyError:
            tokens.append(Token(char, G['symbol']))
        
    tokens.append(Token('$', G.EOF))
    return tokens

def build_grammar():
    G = Grammar()

    E = G.NonTerminal('E', True)
    T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

    # > PRODUCTIONS???
    E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]

    X %= pipe + T + X, lambda h, s: s[3], None, None, lambda h, s: UnionNode(h[0], s[2])
    X %= G.Epsilon, lambda h, s: h[0]

    T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]

    Y %= F + Y, lambda h, s: s[2], None, lambda h, s: ConcatNode(h[0], s[1])
    Y %= G.Epsilon, lambda h, s: h[0]

    F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]

    Z %= star, lambda h, s: ClosureNode(h[0]), None
    Z %= G.Epsilon, lambda h, s: h[0]

    A %= epsilon, lambda h, s: EpsilonNode(s[1]), None
    A %= symbol, lambda h, s: SymbolNode(s[1]), None
    A %= opar + E + cpar, lambda h, s: s[2], None, None, None
    
    return G

G=build_grammar()

L=metodo_predictivo_no_recursivo(G)

class Regex:
    def __init__(self,regex,skip_whitespaces=False):
        W=self
        W.regex=regex
        W.automaton=W.build_automaton(regex)
        
    def __call__(self,text):
        W=self
        return W.automaton.recognize(text)
    
    @staticmethod
    def build_automaton(regex,skip_whitespaces=False):
        h=regex_tokenizer(regex,G,skip_whitespaces=False)
        f=L(h)
        T=evaluate_parse(f,h)
        H=T.evaluate()
        X=nfa_to_dfa(H)
        k=automata_minimization(X)
        return k