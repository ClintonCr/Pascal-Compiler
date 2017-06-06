# Token Types
# Following Rusland Lets build a compiler
# EOF (end-of-title) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, PLUS, EOF, MINUS = 'INTEGER', 'PLUS', 'EOF', 'MINUS'

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

class Interpreter(object):
	def __init__(self, text):
		# client string input, e.g. "3+5"
		self.text = text
		#self.pos is an ndex into self.text
		self.pos = 0
		# current token instance
		self.current_token = None
		# sets current char to the respective position in the text
	        self.current_Char = self.text[self.pos]

	def error(self):
		raise exception('Error parsing input')

	def next_Char(self):
		self.pos += 1
		
		if self.pos > len(self.text) -1:
			self.current_Char = None
		else:
			self.current_Char = self.text[self.pos]

	def skip_Whitespace(self):
		while self.current_Char is not None and self.current_Char.isspace():
			self.next_Char()
		
	def join_Integer(self):
		
		result = ''
		
		while self.current_Char is not None and self.current_Char.isdigit():
			result += self.current_Char
			self.next_Char()
		return int(result)

	def get_Next_Token(self):
		
		while self.current_Char is not None:

			if self.current_Char.isspace():
				self.skip_Whitespace()
				continue

			if self.current_Char.isdigit():
				return Token(INTEGER, self.join_Integer())

			if self.current_Char == '+':
				self.next_Char()
				return Token(PLUS, self.current_Char)

			if self.current_Char == '-':
				self.next_Char()
				return Token(MINUS, self.current_Char)

			self.error()
		
		return Token(EOF, None)

	def eat(self, token_Type):
		# compare the current token type with the passed token
		# type and if they match then "eat" the current token
		# and assign the next token to the self.currentToken,
		# otherwise raise an exception.
		if self.current_Token.type == token_Type:
			self.current_Token = self.get_Next_Token()
		else:
			self.error()

	def expr(self):
		"""expr -> INTEGER PLUS INTEGER"""
		# set current token to the first token taken from the input
		self.current_Token = self.get_Next_Token()

		# we expect the current token to be a single-digit integer
		left = self.current_Token
		self.eat(INTEGER)

		# we expect the current token to be a '+' token
		op = self.current_Token

		if op.type == PLUS:
			self.eat(PLUS)
		else:
			self.eat(MINUS)

		#we expect the current token to be a single-digit integer
		right = self.current_Token
		self.eat(INTEGER)
		# after the above call the self.currentToken is set to
		# EOF token

		# at this point INTEGER PLUS INTEGER sequence of tokens
		# has been successfully found and the method can just
		# return the result of adding two integers, thus
		# effectively interpreting client input
		if op.type == PLUS:
			result = left.value + right.value
		else:
			result = left.value - right.value
		return result

def main():
	while True:
		try:
			# To run under Python3 replace 'rawInput' call
			# with 'input'
			text = raw_input('calc> ')
		except EOFError:
			break
		if not text:
			continue
		interpreter = Interpreter(text)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
	main()


