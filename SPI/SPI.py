# Token Types
# Following Rusland Lets build a compiler
# EOF (end-of-title) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, PLUS, MINUS, MUL, DIV, LBRACKET, RBRACKET, EOF, BEGIN, END, DOT, ASSIGN, SEMI, ID = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'BEGIN', 'END', 'DOT', 'ASSIGN', 'SEMI', 'ID'
)
class Token(object):
    def __init__(self, type, value):
        
        #token type: INTEGER, PLUS or EOF
        self.type = type
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-' or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

RESERVE_KEYWORDS = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END')
}

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        #self.pos is an ndex into self.text
        self.pos = 0
        # current token instance
        #self.current_token = None
        # sets current char to the respective position in the text
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def next_char(self):
        self.pos += 1
        
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) + 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_Whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next_char()

    def join_Integer(self):
        
        result = ''
        
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.next_char()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char.upper()
            self.next_char()

        token = RESERVE_KEYWORDS.get(result,Token(ID,result))
        return token

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_Whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.join_Integer())

            if self.current_char.isalnum():
                return self._id()

            if self.current_char == ':' and self.peek() == '=':
                self.next_char()
                self.next_char()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.next_char()
                return Token(SEMI,';')

            if self.current_char == '+':
                self.next_char()
                return Token(PLUS, self.current_char)

            if self.current_char == '-':
                self.next_char()
                return Token(MINUS, self.current_char)

            if self.current_char == '*':
                self.next_char()
                return Token(MUL, self.current_char)

            if self.current_char == '/':
                self.next_char()
                return Token(DIV, self.current_char)

            if self.current_char == '(':
                self.next_char()
                return Token(LBRACKET, '(')

            if self.current_char == ')':
                self.next_char()
                return Token(RBRACKET, ')')

            if self.current_char == '.':
                self.next_char()
                return Token(DOT, '.')


            self.error()
        
        return Token(EOF, None)


class AST(object):
    pass

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self,op,expr):
        self.token = self.op = op
        self.expr = expr

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value.upper()

class NoOp(AST):
    pass

class Parser(object):
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.currentToken,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def program(self):
        
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left,token,right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def factor(self):

        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token

        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LBRACKET:
            self.eat(LBRACKET)
            node = self.expr()
            self.eat(RBRACKET)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node,op=token,right=self.factor())

        return node
        
    def expr(self):
            
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token

            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node,op=token,right=self.term())

        return node

    def parse(self):
        node = self.program()

        if self.current_token.type != EOF:
            self.error()

        return node


class NodeVisitor(object):
    def visit(self,node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)

    def generic_visit(self,node):
        raise Exception('No Visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}
    
    def __init__(self,parser):
        self.parser = parser

    def visit_BinOp(self,node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self,node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self,node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self,node):
        pass

    def visit_Assign(self,node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name.upper()] = self.visit(node.right)

    def visit_Var(self,node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    import sys
    text = open(sys.argv[1],'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)

if __name__ == '__main__':
    main()