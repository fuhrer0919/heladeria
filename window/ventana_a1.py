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
            QPushButton#btn_guardar_form, QPushButton#btn_atras_form {
                background-color: #4A90E2;
                border: 3px solid #2C5282;
                border-radius: 16px;
                color: white;
                padding: 0px;
                font-size: 26px;
                font-weight: bold;
                min-width: 320px;
                max-width: 320px;
                min-height: 56px;
                max-height: 56px;
            }
            QPushButton#btn_guardar_form:hover, QPushButton#btn_atras_form:hover {
                background-color: #2C5282;
            }
            QPushButton#btn_guardar_form:pressed, QPushButton#btn_atras_form:pressed {
                background-color: #1e3a5f;
            }
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Contenido con scroll: evita que los botones se compriman en 600px de alto
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: #E6F3FF; }")

        scroll_inner = QtWidgets.QWidget()
        scroll_inner.setStyleSheet("background-color: #E6F3FF;")
        self.form_layout = QtWidgets.QVBoxLayout(scroll_inner)
        self.form_layout.setContentsMargins(16, 12, 16, 16)
        self.form_layout.setSpacing(0)

        # Título
        self.title_label = QtWidgets.QLabel("Formulario de Aseo y Desinfeccion")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.form_layout.addWidget(self.title_label)

        self.form_layout.addSpacing(16)

        # Fecha
        self.fecha_label = QtWidgets.QLabel("Fecha:")
        self.form_layout.addWidget(self.fecha_label)
        self.fecha_edit = QtWidgets.QDateEdit()
        self.fecha_edit.setDate(QtCore.QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        self.form_layout.addWidget(self.fecha_edit)

        self.form_layout.addSpacing(10)

        # Usuario
        self.usuario_label = QtWidgets.QLabel("Usuario:")
        self.form_layout.addWidget(self.usuario_label)
        self.usuario_combo = QtWidgets.QComboBox()
        usuarios = db_helper.get_usuarios()
        for uid, nombre in usuarios:
            self.usuario_combo.addItem(nombre, uid)
        ultimo_usuario = db_helper.get_ultimo_usuario_aseo()
        if ultimo_usuario:
            for i in range(self.usuario_combo.count()):
                if self.usuario_combo.itemData(i) == ultimo_usuario:
                    self.usuario_combo.setCurrentIndex(i)
                    break
        self.form_layout.addWidget(self.usuario_combo)

        self.form_layout.addSpacing(10)

        # Elemento
        self.elemento_label = QtWidgets.QLabel("Elemento:")
        self.form_layout.addWidget(self.elemento_label)
        self.elemento_combo = QtWidgets.QComboBox()
        elementos = db_helper.get_elementos()
        for eid, elemento in elementos:
            self.elemento_combo.addItem(elemento, eid)
        self.form_layout.addWidget(self.elemento_combo)

        self.form_layout.addSpacing(16)

        # Checkboxes para actividades
        self.actividades_label = QtWidgets.QLabel("Actividades realizadas:")
        self.form_layout.addWidget(self.actividades_label)

        self.desinfeccion_check = QtWidgets.QCheckBox("Desinfeccion")
        self.form_layout.addWidget(self.desinfeccion_check)

        self.lavado_check = QtWidgets.QCheckBox("Lavado")
        self.form_layout.addWidget(self.lavado_check)

        self.barrido_check = QtWidgets.QCheckBox("Barrido")
        self.form_layout.addWidget(self.barrido_check)

        self.trapeado_check = QtWidgets.QCheckBox("Trapeado")
        self.form_layout.addWidget(self.trapeado_check)

        self.evacuacion_check = QtWidgets.QCheckBox("Evacuacion de Basuras")
        self.form_layout.addWidget(self.evacuacion_check)

        self.form_layout.addSpacing(16)

        # Observaciones
        self.obs_label = QtWidgets.QLabel("Observaciones:")
        self.form_layout.addWidget(self.obs_label)
        self.obs_edit = QtWidgets.QTextEdit()
        self.obs_edit.setMaximumHeight(80)
        self.obs_edit.textChanged.connect(self.limitar_observaciones)
        self.form_layout.addWidget(self.obs_edit)

        self.scroll.setWidget(scroll_inner)
        self.main_layout.addWidget(self.scroll, 1)

        # Barra inferior fija: botones siempre visibles y tamaño estable
        self.button_bar = QtWidgets.QFrame()
        self.button_bar.setFixedHeight(96)
        self.button_bar.setStyleSheet(
            "QFrame { background-color: #d6e8fb; border-top: 2px solid #4A90E2; }"
        )
        self.button_layout = QtWidgets.QHBoxLayout(self.button_bar)
        self.button_layout.setSpacing(40)
        self.button_layout.setContentsMargins(24, 16, 24, 16)
        self.button_layout.addStretch(1)

        self.guardar_btn = QtWidgets.QPushButton("Guardar")
        self.guardar_btn.setObjectName("btn_guardar_form")
        self.guardar_btn.setFixedSize(320, 56)
        self.guardar_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.guardar_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.guardar_btn.clicked.connect(self.guardar_aseo)
        self.button_layout.addWidget(self.guardar_btn)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.setObjectName("btn_atras_form")
        self.atras_btn.setFixedSize(320, 56)
        self.atras_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.atras_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.atras_btn.clicked.connect(self.volver_a_f1)
        self.button_layout.addWidget(self.atras_btn)

        self.button_layout.addStretch(1)
        self.main_layout.addWidget(self.button_bar, 0)

        # Misma resolución que ventana_main.py (1024x600); fijar tras el layout para la Raspberry
        self.setFixedSize(1024, 600)

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