import os.path


class Scanner :
    token_type = ['SEMICOLON', 'IF', 'THEN', 'END', 'REPEAT',
                'UNTIL', 'IDENTIFIER', 'ASSIGN', 'READ',
                'WRITE', 'LESSTHAN', 'EQUAL', 'PLUS', 'MINUS',
                'MULT', 'DIV', 'OPENBRACKET', 'CLOSEDBRACKET', 'NUMBER'
                ]
    token_value = [';', 'if', 'then', 'end', 'repeat',
                'until', -1 , ':=', 'read',
                'write', '<', '=', '+', '-',
                '*', '/', '(', ')', -1
                ]

    @staticmethod
    def generate_tokens(input_string):
        str = ""
        list = []
        input_string = Scanner.remove_comments(input_string)
        input_string = input_string.replace(";"," ; ")
        input_string = input_string.replace("(", " ( ")
        input_string = input_string.replace(")", " ) ")

        items_list = input_string.split()
        for i in range(len(items_list)):
            if items_list[i] in Scanner.token_value:
                index_item = Scanner.token_value.index(items_list[i])
                str += f'{Scanner.token_value[index_item]},{Scanner.token_type[index_item]} \n'
                list.append(Scanner.token_type[index_item])
                list.append(Scanner.token_value[index_item])
            else:
                special_items = items_list[i]
                if special_items.isnumeric():
                    str += f'{special_items},{"NUMBER"} \n'
                    list.append('NUMBER')
                    list.append(special_items)

                else:
                    str += f'{special_items},{"IDENTIFIER"} \n'
                    list.append('IDENTIFIER')
                    list.append(special_items)
                if ';' in items_list[i]:
                    str += f';,{"SEMICOLON"} \n'
                    list.append('SEMICOLON')
                    list.append(';')

        Scanner.write_file(str)


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
    def write_file (input_string):
        if os.path.isfile("output.txt"):
            os.remove("output.txt")
        f = open("output.txt", "w")
        f.write(input_string)


