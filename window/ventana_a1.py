# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import db_helper


class Ui_FormularioAseo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("FormularioAseo")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Formulario de Aseo y Desinfeccion")

        # Establecer el color de fondo
        self.setStyleSheet("""
            QWidget {
                background-color: #E6F3FF;
            }
            QLabel {
                color: #1A365D;
                font-size: 18px;
            }
            QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit, QCheckBox {
                background-color: white;
                border: 2px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QCheckBox {
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QPushButton {
                background-color: #4A90E2;
                border: 3px solid #2C5282;
                border-radius: 15px;
                color: white;
                padding: 10px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #2C5282;
            }
        """)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Título
        self.title_label = QtWidgets.QLabel("Formulario de Aseo y Desinfeccion")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.layout.addSpacing(20)

        # Fecha
        self.fecha_label = QtWidgets.QLabel("Fecha:")
        self.layout.addWidget(self.fecha_label)
        self.fecha_edit = QtWidgets.QDateEdit()
        self.fecha_edit.setDate(QtCore.QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        self.layout.addWidget(self.fecha_edit)

        self.layout.addSpacing(10)

        # Usuario
        self.usuario_label = QtWidgets.QLabel("Usuario:")
        self.layout.addWidget(self.usuario_label)
        self.usuario_combo = QtWidgets.QComboBox()
        usuarios = db_helper.get_usuarios()
        for uid, nombre in usuarios:
            self.usuario_combo.addItem(nombre, uid)
        # Seleccionar último usuario si existe
        ultimo_usuario = db_helper.get_ultimo_usuario_aseo()
        if ultimo_usuario:
            for i in range(self.usuario_combo.count()):
                if self.usuario_combo.itemData(i) == ultimo_usuario:
                    self.usuario_combo.setCurrentIndex(i)
                    break
        self.layout.addWidget(self.usuario_combo)

        self.layout.addSpacing(10)

        # Elemento
        self.elemento_label = QtWidgets.QLabel("Elemento:")
        self.layout.addWidget(self.elemento_label)
        self.elemento_combo = QtWidgets.QComboBox()
        elementos = db_helper.get_elementos()
        for eid, elemento in elementos:
            self.elemento_combo.addItem(elemento, eid)
        self.layout.addWidget(self.elemento_combo)

        self.layout.addSpacing(20)

        # Checkboxes para actividades
        self.actividades_label = QtWidgets.QLabel("Actividades realizadas:")
        self.layout.addWidget(self.actividades_label)

        self.desinfeccion_check = QtWidgets.QCheckBox("Desinfeccion")
        self.layout.addWidget(self.desinfeccion_check)

        self.lavado_check = QtWidgets.QCheckBox("Lavado")
        self.layout.addWidget(self.lavado_check)

        self.barrido_check = QtWidgets.QCheckBox("Barrido")
        self.layout.addWidget(self.barrido_check)

        self.trapeado_check = QtWidgets.QCheckBox("Trapeado")
        self.layout.addWidget(self.trapeado_check)

        self.evacuacion_check = QtWidgets.QCheckBox("Evacuacion de Basuras")
        self.layout.addWidget(self.evacuacion_check)

        self.layout.addSpacing(20)

        # Observaciones
        self.obs_label = QtWidgets.QLabel("Observaciones:")
        self.layout.addWidget(self.obs_label)
        self.obs_edit = QtWidgets.QTextEdit()
        self.obs_edit.setMaximumHeight(80)
        self.obs_edit.textChanged.connect(self.limitar_observaciones)
        self.layout.addWidget(self.obs_edit)

        self.layout.addStretch()

        # Botones
        self.button_layout = QtWidgets.QHBoxLayout()

        self.guardar_btn = QtWidgets.QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.guardar_aseo)
        self.button_layout.addWidget(self.guardar_btn)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.clicked.connect(self.volver_a_f1)
        self.button_layout.addWidget(self.atras_btn)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def guardar_aseo(self):
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        id_usuario = self.usuario_combo.currentData()
        id_elemento = self.elemento_combo.currentData()
        desinfeccion = 1 if self.desinfeccion_check.isChecked() else 0
        lavado = 1 if self.lavado_check.isChecked() else 0
        barrido = 1 if self.barrido_check.isChecked() else 0
        trapeado = 1 if self.trapeado_check.isChecked() else 0
        evacuacion = 1 if self.evacuacion_check.isChecked() else 0
        observaciones = self.obs_edit.toPlainText()

        if not id_usuario or not id_elemento:
            QMessageBox.warning(self, "Error", "Selecciona un usuario y un elemento.")
            return

     # Verificar que al menos una actividad esté seleccionada
        if not (desinfeccion or lavado or barrido or trapeado or evacuacion):
            QMessageBox.warning(self, "Error", "Debes seleccionar al menos una actividad realizada.")
            return

        success = db_helper.insertar_aseo(fecha, id_usuario, id_elemento, desinfeccion, lavado, barrido, trapeado, evacuacion, observaciones)
        if success:
            QMessageBox.information(self, "Éxito", "Registro de aseo guardado correctamente.")
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", "Error al guardar el registro.")

    def limpiar_formulario(self):
        self.fecha_edit.setDate(QtCore.QDate.currentDate())
        self.usuario_combo.setCurrentIndex(0)
        self.elemento_combo.setCurrentIndex(0)
        self.desinfeccion_check.setChecked(False)
        self.lavado_check.setChecked(False)
        self.barrido_check.setChecked(False)
        self.trapeado_check.setChecked(False)
        self.evacuacion_check.setChecked(False)
        self.obs_edit.clear()

    def limitar_observaciones(self):
        text = self.obs_edit.toPlainText()
        if len(text) > 100:
            self.obs_edit.blockSignals(True)
            self.obs_edit.setPlainText(text[:100])
            self.obs_edit.moveCursor(QtGui.QTextCursor.End)
            self.obs_edit.blockSignals(False)

    def volver_a_f1(self):
        if self.parent_window is not None:
            self.parent_window.show()
            self.close()
        else:
            self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormularioAseo()
    window.show()
    sys.exit(app.exec_())