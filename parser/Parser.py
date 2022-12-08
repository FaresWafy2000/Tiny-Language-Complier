

class Node :


    def __init__(self,token_value , optional_value=None):
        self.token_value = token_value
        self.optional_value = optional_value
        self.children = []
        self.siblings = None

class Parser :
    tokens_types = []
    tokens_values = []
    index = 0
    def __init__(self):
        self.parse_tree = None
        self.token_value = self.tokens_values[0]
        print(self.token_value)

    def statment_sequence(self):
        parent = self.statment_grammer()
        temp = parent
        while self.is_next_token_valid():
            child = self.statment_grammer()
            if child is not None:
                parent.siblings = child
                parent = child
            if self.token_value == 'end' or self.token_value == 'until' :
                return temp
        return temp

    def if_stmt(self):
        t = Node('if', self.tokens_values[self.index])
        if self.token_value == 'if':
            self.token_matching('IF')
            t.children.append(self.exp())
            self.token_matching('THEN')
            t.children.append(self.statment_sequence())
            if (self.token_value == ';') :
                self.next_token()

            if self.token_value == 'else':
                self.token_matching('ELSE')
                t.children.append(self.statment_sequence())
            self.token_matching('END')
        return t
    @staticmethod
    def print_tree(root):
        if root is not None :
            print(f"token value {root.token_value} optional value if requried {root.optional_value} \n")
            if (root.siblings is not None):
                print("siblings")
                Parser.print_tree(root.siblings)
            if len(root.children) != 0:
                print("child")
                for i in range (len(root.children)):
                    Parser.print_tree(root.children[i])


    def token_matching(self,token_type):
        if self.tokens_types[self.index] == token_type:
            self.next_token()
            return True
        else:
            print("error")
            raise ValueError('Token Mismatch', self.token_value)
    def is_next_token_valid(self):
        if self.index < len(self.tokens_values) :
            return True
        return False
    def next_token(self):
        if (self.index == len(self.tokens_values) - 1):
            self.index = self.index+1
            return False
        self.index = self.index + 1
        self.token_value = self.tokens_values[self.index]
        return True

    def statment_grammer(self):
        if self.token_value == 'read':
            node = self.read_grammer()
            return node

        if self.token_value == 'write':
            node = self.write_grammer()
            return node
        if self.token_value == 'if':
            node = self.if_stmt()
            return node
        if self.token_value == 'repeat':
            node = self.repeat_stmt()
            return node
        if self.tokens_types[self.index] == 'IDENTIFIER':
            node = self.assign_grammer()
            return node
        if self.token_value == 'end':
            return

        self.next_token()

    def read_grammer(self):
        parent = Node ('read',self.tokens_values[self.index+1])
        self.token_matching('READ')
        self.index = self.index +1
        return parent
    def write_grammer(self):
        parent = Node ('write')
        self.token_matching('WRITE')
        parent.children.append(Node('identifier',self.tokens_values[self.index]))
        self.token_matching('IDENTIFIER')
        return parent

    def assign_grammer(self):
        node=Node('assign',self.tokens_values[self.index])
        self.token_matching('IDENTIFIER')
        self.token_matching('ASSIGN')
        node.children.append(self.exp())
        return node

    def exp(self):
        t = self.simple_exp()
        if self.token_value == '<' or self.token_value == '>' or self.token_value == '=':
            p = Node('op', self.tokens_values[self.index])
            p.children.append(t)
            t = p
            self.comparison_op()
            t.children.append(self.simple_exp())
        return t

    def comparison_op(self):
        if self.token_value == '<':
            self.token_matching('LESSTHAN')
        elif self.token_value == '>':
            self.token_matching('GREATERTHAN')
        elif self.token_value == '=':
            self.token_matching('EQUAL')

    def simple_exp(self):
        t = self.term()
        while self.token_value == '+' or self.token_value == '-':
            p = Node('Opk', self.tokens_values[self.index])
            p.children.append(t)
            t = p
            self.addop()
            t.children.append(self.term())
        return t

    def addop(self):
        if self.token_value == '+':
            self.token_matching('PLUS')
        elif self.token_value == '-':
            self.token_matching('MINUS')

    def term(self):
        t = self.factor()
        while self.token_value == '*' or self.token_value == '/':
            p = Node('Opk', self.tokens_values[self.index])
            p.children.append(t)
            t = p
            self.mulop()
            p.children.append(self.factor())
        return t



    def repeat_stmt(self):
        t = Node('repeat', self.tokens_values[self.index])
        if self.token_value == 'repeat':
            self.token_matching('REPEAT')
            t.children.append(self.statment_sequence())
            if self.token_value == ';':
                self.next_token()
            self.token_matching('UNTIL')
            t.children.append(self.exp())
        return t

    def mulop(self):
        if self.token_value == '*':
            self.token_matching('MULT')
        elif self.token_value == '/':
            self.token_matching('DIV')

    def factor(self):
        if self.token_value == '(':
            self.token_matching('OPENBRACKET')
            t = self.exp()
            self.token_matching('CLOSEDBRACKET')
        elif self.tokens_types[self.index] == 'NUMBER':
            t = Node('ConstK', self.tokens_values[self.index])
            self.token_matching('NUMBER')
        elif self.tokens_types[self.index] == 'IDENTIFIER':
            t = Node('Idk', self.tokens_values[self.index])
            self.token_matching('IDENTIFIER')
        else:
            raise ValueError('SyntaxError', self.token_value)
            return False
        return t