from PyQt5 import QtWidgets
from window.ventana_main import Ui_main

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())


    # fake_gpio.py

class GPIO:
    BCM = 'BCM'
    BOARD = 'BOARD'
    OUT = 'OUT'
    IN = 'IN'
    HIGH = 1
    LOW = 0

    @staticmethod
    def setmode(mode):
        print(f"[FAKE GPIO] setmode({mode})")

    @staticmethod
    def setup(pin, mode):
        print(f"[FAKE GPIO] setup(pin={pin}, mode={mode})")

    @staticmethod
    def output(pin, value):
        print(f"[FAKE GPIO] output(pin={pin}, value={value})")

    @staticmethod
    def cleanup():
        print("[FAKE GPIO] cleanup()")

