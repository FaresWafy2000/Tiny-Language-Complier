
import Scanner
from parser.Parser import Parser, Node

input_string = Scanner.Scanner.read_file()
list1,list2 = Scanner.Scanner.generate_tokens(input_string)
Parser.tokens_types = list1
Parser.tokens_values = list2
p1 = Parser()
x=p1.statment_sequence()
Parser.print_tree(x)



