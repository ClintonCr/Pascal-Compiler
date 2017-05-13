# Token Types
#
# EOF (end-of-title) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token(object):
	def __init__(self, type, value):
		
		#token type: INTEGER, PLUS or EOF
		self.type = type
		# token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', or None
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

	def error(self):
		raise exception('Error parsing input')

	def get_Next_Token(self):
		"""Lexical analyser (also known as scanner or tokenizer)

		This method is responsible for breaking a sentence aart 		into tokens. One token at a time.
		"""
		text = self.text

		# is self.pos index past the end of the self.text?
		# if so, then return EOF token because there is no more
		# input left to convert into tokens.
		if self.pos > len(text) - 1:
			return Token(EOF, None)

		# get a character at the position self.pos and decide
		# what token to create based on the single character
		current_Char = text[self.pos]

		# if the character is a digit then convert it to
		# integer, create an INTEGER token, increment self.pos
		# index to point to the next character after the digit,
		# and return the INTEGER token.
		if current_Char.isdigit():
			token = Token(INTEGER, int(current_Char))
			self.pos += 1
			return token

		if current_Char == '+':
			token = Token(PLUS, current_Char)
			self.pos += 1
			return token

		self.error()

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
		self.eat(PLUS)

		#we expect the current token to be a single-digit integer
		right = self.current_Token
		self.eat(INTEGER)
		# after the above call the self.currentToken is set to
		# EOF token

		# at this point INTEGER PLUS INTEGER sequence of tokens
		# has been successfully found and the method can just
		# return the result of adding two integers, thus
		# effectively interpreting client input
		result = left.value + right.value
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


