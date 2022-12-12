from drawing.drawer import Drawer


class Node :


    def __init__(self,token_value , optional_value=None):
        self.token_value = token_value
        self.optional_value = optional_value
        self.children = []
        self.siblings = None
        self.index = Parser.index
        self.shape = 's'

class Parser :
    tokens_types = []
    tokens_values = []
    nodes_table={}
    edges_table = []

    index = 0
    def __init__(self):
        self.parse_tree = None
        print(len(self.tokens_values))
        self.token_value = self.tokens_values[0]
        self.nodes_table = None
        self.edges_table = None
        self.same_rank_nodes = []
        print(self.token_value)

    def statment_sequence(self):
        parent = self.statment_grammer()
        head = parent
        while self.is_next_token_valid():
            brother = self.statment_grammer()
            if brother is not None:
                parent.siblings = brother
                parent = brother
            if self.token_value == 'end' or self.token_value == 'until' :
                return head
        self.parse_tree =head
        return head

    def if_stmt(self):
        t = Node('if', "")
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
        parent.optional_value=''
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
            p = Node('operator', self.tokens_values[self.index])
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
            p = Node('Operator', self.tokens_values[self.index])
            p.shape ='o'
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
            p = Node('Operator', self.tokens_values[self.index])
            p.shape='o'
            p.children.append(t)
            t = p
            self.mulop()
            p.children.append(self.factor())
        return t



    def repeat_stmt(self):
        t = Node('repeat',"")
        
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
            t = Node('Constant', self.tokens_values[self.index])

            self.token_matching('NUMBER')
        elif self.tokens_types[self.index] == 'IDENTIFIER':
            t = Node('Identifier', self.tokens_values[self.index])
            self.token_matching('IDENTIFIER')
        else:
            raise ValueError('SyntaxError', self.token_value)
            return False
        t.shape = 'o'
        return t

    def create_nodes_table(self, args=None):  # create the nodes table
        if args == None:  # check if the function is called for the first time
            self.parse_tree.index = Parser.index  # set the index of the node
            Parser.nodes_table.update(
                {Parser.index: [self.parse_tree.token_value, self.parse_tree.optional_value,
                                self.parse_tree.shape]})  # add the node to the nodes table
            Parser.index = Parser.index + 1  # increment the index
            if len(self.parse_tree.children) != 0:  # check if the node has children
                for i in self.parse_tree.children:  # loop on the children
                    self.create_nodes_table(i)  # call the function recursively
            if self.parse_tree.siblings != None:  # check if the node has a sibling
                self.create_nodes_table(self.parse_tree.siblings)  # call the function recursively
        else:  # if the function is called recursively
            args.index = Parser.index  # set the index of the node
            Parser.nodes_table.update(
                {Parser.index: [args.token_value, args.optional_value, args.shape]})  # add the node to the nodes table
            Parser.index = Parser.index + 1  # increment the index
            if len(args.children) != 0:  # check if the node has children
                for i in args.children:  # loop on the children
                    self.create_nodes_table(i)  # call the function recursively
            if args.siblings != None:  # check if the node has a sibling
                self.create_nodes_table(args.siblings)  # call the function recursively

    def create_edges_table(self, args=None):  # create the edges table
        if args == None:  # check if the function is called for the first time
            if len(self.parse_tree.children) != 0:  # check if the node has children
                for i in self.parse_tree.children:  # loop on the children
                    Parser.edges_table.append((self.parse_tree.index, i.index))  # add the edge to the edges table
                for j in self.parse_tree.children:  # loop on the children
                    self.create_edges_table(j)  # call the function recursively
            if self.parse_tree.siblings != None:  # check if the node has a sibling
                Parser.edges_table.append(
                    (self.parse_tree.index, self.parse_tree.siblings.index))  # add the edge to the edges table
                self.same_rank_nodes.append(
                    [self.parse_tree.index, self.parse_tree.siblings.index])  # add the nodes to the same_rank_nodes list
                self.create_edges_table(self.parse_tree.siblings)  # call the function recursively
        else:  # if the function is called recursively
            if len(args.children) != 0:  # check if the node has children
                for i in args.children:  # loop on the children
                    Parser.edges_table.append((args.index, i.index))  # add the edge to the edges table
                for j in args.children:  # loop on the children
                    self.create_edges_table(j)  # call the function recursively
            if args.siblings != None:  # check if the node has a sibling
                Parser.edges_table.append((args.index, args.siblings.index))  # add the edge to the edges table
                self.same_rank_nodes.append(
                    [args.index, args.siblings.index])  # add the nodes to the same_rank_nodes list
                self.create_edges_table(args.siblings)  # call the function recursively

    def clear_tables(self):  # clear the tables
        self.nodes_table.clear()  # clear the nodes_table
        self.edges_table.clear()  # clear the edges_table
    def run(self):  # run the parser

        self.parse_tree = self.statment_sequence()  # create parse tree
        self.create_nodes_table()  # create nodes_table
        self.create_edges_table()  # create edges_table
        self.edges_table = Parser.edges_table  # save edges_table
        self.nodes_table = Parser.nodes_table  # save nodes_table

        # raise ValueError('SyntaxError', self.token) # raise an error if the parser is not successful
        d1 = Drawer()

        d1.Draw(Parser.nodes_table,Parser.edges_table,self.same_rank_nodes)
        self.clear_tables()

