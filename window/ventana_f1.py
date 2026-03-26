# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormularioF1(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("FormularioF1")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Formularios - Aseo e Insumos")

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

        self.title_label = QtWidgets.QLabel("Selecciona un formulario")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(20)

        self.form_aseo_btn = QtWidgets.QPushButton("Formulario Aseo y Desinfeccion")
        self.form_aseo_btn.setObjectName("form_aseo_btn")
        self.form_aseo_btn.setFixedWidth(650)
        self.form_aseo_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.form_aseo_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.form_insumos_btn = QtWidgets.QPushButton("Formulario Control de Insumos")
        self.form_insumos_btn.setObjectName("form_insumos_btn")
        self.form_insumos_btn.setFixedWidth(650)
        self.form_insumos_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.form_insumos_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(40)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.setObjectName("atras_btn")
        self.atras_btn.setFixedWidth(300)
        self.atras_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.atras_btn, alignment=QtCore.Qt.AlignCenter)

        self.layout.addStretch()

        # Conexiones placeholder (a implementar por la app principal)
        self.form_aseo_btn.clicked.connect(self.open_aseo)
        self.form_insumos_btn.clicked.connect(self.open_insumos)
        self.atras_btn.clicked.connect(self.volver_a_main)

        self.setLayout(self.layout)

    def open_aseo(self):
        QtWidgets.QMessageBox.information(self, "Formulario", "Abrir formulario de Aseo y Desinfeccion")

    def open_insumos(self):
        QtWidgets.QMessageBox.information(self, "Formulario", "Abrir formulario de Control de Insumos")

    def volver_a_main(self):
        if self.parent_window is not None:
            self.parent_window.show()
            self.close()
        else:
            # En caso de que no haya ventana padre, cierra solo la ventana actual
            self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormularioF1()
    window.show()
    sys.exit(app.exec_())
