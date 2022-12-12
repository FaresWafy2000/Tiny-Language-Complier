from tkinter import filedialog

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

import Scanner
from Parser import Parser
from frontend import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
# input_string = Scanner.Scanner.read_file()
# list1,list2,p = Scanner.Scanner.generate_tokens(input_string)
# Parser.tokens_types = list1
# Parser.tokens_values = list2
# print(list1)
# print(list2)
# p1 = Parser()
# p1.run()

# print(p1.same_rank_nodes)
#Parser.print_tree(x)
class controllerGUI(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listWidget.setWindowTitle("Problem Table ")

        self.ui.pushButton_2.clicked.connect(self.get_tokens)
        self.ui.pushButton.clicked.connect(self.draw)
        self.ui.actionLoad_File.triggered.connect(self.load)
        
    def get_tokens(self):
       # self.ui.textEdit_2.insertPlainText("aaaaaaaaaaa")
        str1 = self.ui.textEdit_2.toPlainText()
        print(str1)
        x,z,str1,error_flag,error_list = Scanner.Scanner.generate_tokens(str1)
        self.ui.textEdit.clear()

        if error_flag:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Invalid token go to problem table ')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.ui.listWidget.clear()
            for i in range (len(error_list)):
                 self.ui.listWidget.addItem(f"{error_list[i]} is  invalid token ")


        else :
           self.ui.listWidget.clear()
           self.ui.textEdit.append(str1)

    def load(self):

            global directory_path
            file_name = filedialog.askopenfile().close
            s= file_name.read()
            print(s)
            print(Scanner.Scanner.generate_tokens(s))
            self.ui.textEdit_2.clear()
            self.ui.textEdit_2.append(s)

    def draw(self):
        str1 = self.ui.textEdit_2.toPlainText()
        list1,list2,p,x,z = Scanner.Scanner.generate_tokens(str1)
        if len(list1) == 0 :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Invalid token go to problem table ')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.ui.listWidget.clear()
        else :    
            Parser.tokens_types = list1
            Parser.tokens_values = list2
            print(list1)
            print(list2)
            p1 = Parser()
            p1.run()


if __name__=="__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myform = controllerGUI()
    myform.show()
    sys.exit(app.exec_())