import os.path

from Parser import Parser


class Scanner:
    token_type = ['SEMICOLON', 'IF', 'THEN', 'END', 'REPEAT',
                'UNTIL', 'IDENTIFIER', 'ASSIGN', 'READ',
                'WRITE', 'LESSTHAN', 'GREATERTHAN', 'EQUAL', 'PLUS', 'MINUS',
                'MULT', 'DIV', 'OPENBRACKET', 'CLOSEDBRACKET', 'NUMBER'
                ]
    token_value = [';', 'if', 'then', 'end', 'repeat',
                'until', -1 , ':=', 'read',
                'write', '<', '>','=', '+', '-',
                '*', '/', '(', ')', -1
                ]

    @staticmethod
    def generate_tokens(input_string):
        flag = False
        str = ""
        token_type_list = []
        token_value_list = []
        error_list = []
        input_string = Scanner.remove_comments(input_string)
        input_string = Scanner.space_maker(input_string)
        items_list = input_string.split()
        for i in range(len(items_list)):
            if items_list[i] in Scanner.token_value:
                index_item = Scanner.token_value.index(items_list[i])
                str += f'{Scanner.token_value[index_item]},{Scanner.token_type[index_item]} \n'
                token_type_list.append(Scanner.token_type[index_item])
                token_value_list.append(Scanner.token_value[index_item])
            else:
                special_items = items_list[i]
                if special_items.isnumeric():
                    str += f'{special_items},{"NUMBER"} \n'
                    token_type_list.append('NUMBER')
                    token_value_list.append(special_items)

                else:
                    if not special_items.isalpha() :
                        print(f"{special_items} IS NOT VALID TOKEN")
                        str += f'{special_items},{"NOT VALID TOKEN"} \n'
                        token_type_list.append(-1)
                        token_value_list.append(special_items)
                        error_list.append(special_items)
                        flag = True
                        continue

                    str += f'{special_items},{"IDENTIFIER"} \n'
                    token_type_list.append('IDENTIFIER')
                    token_value_list.append(special_items)


        Scanner.write_file(str)
        return token_type_list,token_value_list,str,flag,error_list




    @staticmethod
    def remove_comments(input_string):
        #input_string = input_string.strip()
        for i in range (len(input_string)):
            if i < len(input_string):
                if input_string[i] == '{' :
                    j = i
                    while input_string[j] != '}' and j < len(input_string) :
                        j= j+1
                    input_string = input_string[:i] + input_string[j+1:]
        return input_string

    @staticmethod
    def space_maker(input_string):
        for i in range(len(Scanner.token_value)):
            if (i == 6 or i == len(Scanner.token_value) - 1):
                continue
            if (Scanner.token_value[i] == ":="):
                input_string = input_string.replace(f"{Scanner.token_value[i]}", " %% ")
            input_string = input_string.replace(f"{Scanner.token_value[i]}", f" {Scanner.token_value[i]} ")
        input_string = input_string.replace("%%", " := ")
        return input_string
    @staticmethod
    def read_file(str=None):

        text_file = open("input_file", "r")
        # read whole file to a string
        data = text_file.read()
        # close file
        text_file.close()
        return data

        # try:
        #     # open text file in read mode
        #     text_file = open(f"{str}", "r")
        #     # read whole file to a string
        #     data = text_file.read()
        #     # close file
        #     text_file.close()
        #     return data
        # except :
        #     print("File Not Found")
        #     inp = input("Please Try again ")
        #     Scanner.read_file(inp)


    @staticmethod
    def write_file (input_string):
        if os.path.isfile("output.txt"):
            os.remove("output.txt")
        f = open("output.txt", "w")
        print("Output file is successfully generated ")
        f.write(input_string)


