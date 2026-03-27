# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from window.ventana_ta import Ui_TablaAseo  # Import tabla aseo
from window.ventana_tm import Ui_TablaMateriasPrimas  # Import tabla materias primas
from window.ventana_tv import Ui_TablaVencimientos  # Import tabla vencimientos


class Ui_FormularioAdmin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("FormularioAdmin")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Administrador")

        self.setStyleSheet("""
            QWidget {
                background-color: #E6F3FF;
            }
            QPushButton {
                background-color: #4A90E2;
                border: 3px solid #2C5282;
                border-radius: 15px;
                color: white;
                padding: 12px;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: #2C5282;
            }
            QLabel {
                color: #1A365D;
                font-size: 34px;
            }
        """)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addStretch()

        self.title_label = QtWidgets.QLabel("Administrador")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(20)

        self.tabla_aseo_btn = QtWidgets.QPushButton("Tabla Control Aseo")
        self.tabla_aseo_btn.setObjectName("tabla_aseo_btn")
        self.tabla_aseo_btn.setFixedWidth(650)
        self.tabla_aseo_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.tabla_aseo_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.tabla_materias_btn = QtWidgets.QPushButton("Tabla Control Materias Primas")
        self.tabla_materias_btn.setObjectName("tabla_materias_btn")
        self.tabla_materias_btn.setFixedWidth(650)
        self.tabla_materias_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.tabla_materias_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.vencimientos_btn = QtWidgets.QPushButton("Control Fechas de Vencimiento")
        self.vencimientos_btn.setObjectName("vencimientos_btn")
        self.vencimientos_btn.setFixedWidth(650)
        self.vencimientos_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.vencimientos_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.modificar_btn = QtWidgets.QPushButton("Modificar Registros")
        self.modificar_btn.setObjectName("modificar_btn")
        self.modificar_btn.setFixedWidth(650)
        self.modificar_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.modificar_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(40)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.setObjectName("atras_btn")
        self.atras_btn.setFixedWidth(300)
        self.atras_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.atras_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addStretch()

        # Conexiones
        self.tabla_aseo_btn.clicked.connect(self.abrir_tabla_aseo)
        self.tabla_materias_btn.clicked.connect(self.abrir_tabla_materias)
        self.vencimientos_btn.clicked.connect(self.abrir_tabla_vencimientos)
        self.modificar_btn.clicked.connect(self.abrir_modificar)
        self.atras_btn.clicked.connect(self.volver_a_main)

        self.setLayout(self.layout)

    def abrir_tabla_aseo(self):
        self.window = Ui_TablaAseo()
        self.window.parent_window = self
        self.window.show()
        self.hide()

    def abrir_tabla_materias(self):
        self.window = Ui_TablaMateriasPrimas()
        self.window.parent_window = self
        self.window.show()
        self.hide()

    def abrir_tabla_vencimientos(self):
        self.window = Ui_TablaVencimientos()
        self.window.parent_window = self
        self.window.show()
        self.hide()

    def abrir_modificar(self):
        QtWidgets.QMessageBox.information(self, "Modificar", "Abrir Modificar Registros")

    def volver_a_main(self):
        if self.parent_window is not None:
            self.parent_window.show()
            self.close()
        else:
            self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormularioAdmin()
    window.show()
    sys.exit(app.exec_())
