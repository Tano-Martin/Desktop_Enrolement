import sys
from PyQt5 import QtWidgets
from widgets.formulaireWidget import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__=="__main__":
    main()
