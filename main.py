import Scanner

inp = input("ENTER FILE PATH ")
input_string = Scanner.Scanner.read_file(inp)
Scanner.Scanner.generate_tokens(input_string)

