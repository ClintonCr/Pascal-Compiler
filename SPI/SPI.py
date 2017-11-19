# Token Types
# Following Rusland Lets build a compiler
# EOF (end-of-title) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, PLUS, MINUS, MUL, DIV, LBRACKET, RBRACKET, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
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

    def skip_Whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next_char()

    def join_Integer(self):
        
        result = ''
        
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.next_char()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_Whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.join_Integer())

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
        

    def factor(self):

        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LBRACKET:
            self.eat(LBRACKET)
            node = self.expr()
            self.eat(RBRACKET)
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
        return self.expr()


class NodeVisitor(object):
    def visit(self,node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)

    def generic_visit(self,node):
        raise Exception('No Visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
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

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        try:
            text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()