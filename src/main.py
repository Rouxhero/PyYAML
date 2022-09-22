import sys
from core import *
from interface import *

chekUpLib()

def main(args):
    monApp=QApplication(args)
    w = Ui_MainWindow()
    title = "PyYAML"
    w.setWindowTitle(title)
    w.setWindowIcon(QIcon('../libs/images/logo.svg'))
    w.show()
    sys.exit(monApp.exec_())

if __name__ == "__main__" : 
    main(["","PyYAML"])