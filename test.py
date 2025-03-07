from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from Visitor import Visitor
import sys

input_stream = FileStream(sys.argv[1])

lexer = ExprLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = ExprParser(token_stream)
tree = parser.root()

visitor = Visitor()
visitor.visit(tree)