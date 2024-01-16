import sys
from PyQt5.QtWidgets import QApplication
from gui import TrigMainWindow

def main():
    '''
    Main function to run the program.
    It creates an instance of the TrigMainWindow class and displays it.
    '''
    app = QApplication(sys.argv)
    gui = TrigMainWindow()
    gui.show()
    sys.exit(app.exec_()) # for clean exit

main()