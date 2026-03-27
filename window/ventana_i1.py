# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import db_helper


class Ui_FormularioMateriasPrimas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("FormularioMateriasPrimas")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Formulario de Control Materias Primas")

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
        self.title_label = QtWidgets.QLabel("Formulario de Control Materias Primas")
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

        # Insumo
        self.insumo_label = QtWidgets.QLabel("Insumo:")
        self.form_layout.addWidget(self.insumo_label)
        self.insumo_combo = QtWidgets.QComboBox()
        insumos = db_helper.get_insumos_filtrados()
        for iid, insumo in insumos:
            self.insumo_combo.addItem(insumo, iid)
        self.form_layout.addWidget(self.insumo_combo)

        self.form_layout.addSpacing(10)

        # Temperatura
        self.temp_label = QtWidgets.QLabel("Temperatura (°C):")
        self.form_layout.addWidget(self.temp_label)
        self.temp_spin = QtWidgets.QSpinBox()
        self.temp_spin.setRange(-50, 100)  # Rango razonable
        self.form_layout.addWidget(self.temp_spin)

        self.form_layout.addSpacing(16)

        # Anomalías
        self.anomalias_label = QtWidgets.QLabel("Anomalías detectadas:")
        self.form_layout.addWidget(self.anomalias_label)

        self.olor_check = QtWidgets.QCheckBox("Olor Extraño")
        self.form_layout.addWidget(self.olor_check)

        self.textura_check = QtWidgets.QCheckBox("Textura Extraña")
        self.form_layout.addWidget(self.textura_check)

        self.color_check = QtWidgets.QCheckBox("Color Extraño")
        self.form_layout.addWidget(self.color_check)

        self.empaque_check = QtWidgets.QCheckBox("Empaque Extraño")
        self.form_layout.addWidget(self.empaque_check)

        self.form_layout.addSpacing(10)

        # Fecha Vencimiento
        self.venc_label = QtWidgets.QLabel("Fecha de Vencimiento:")
        self.form_layout.addWidget(self.venc_label)
        self.venc_edit = QtWidgets.QDateEdit()
        self.venc_edit.setDate(QtCore.QDate.currentDate().addDays(30))  # Default +30 días
        self.venc_edit.setCalendarPopup(True)
        self.form_layout.addWidget(self.venc_edit)

        self.form_layout.addSpacing(10)

        # Observaciones
        self.obs_label = QtWidgets.QLabel("Observaciones:")
        self.form_layout.addWidget(self.obs_label)
        self.obs_edit = QtWidgets.QTextEdit()
        self.obs_edit.setMaximumHeight(80)
        self.obs_edit.textChanged.connect(self.limitar_observaciones)
        self.form_layout.addWidget(self.obs_edit)

        self.scroll.setWidget(scroll_inner)
        self.main_layout.addWidget(self.scroll, 1)

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
        self.guardar_btn.clicked.connect(self.guardar_materias)
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

    def guardar_materias(self):
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        id_insumo = self.insumo_combo.currentData()
        id_tipo = db_helper.get_tipo_insumo_por_insumo(id_insumo)
        temperatura = self.temp_spin.value()
        olor_extraño = 1 if self.olor_check.isChecked() else 0
        textura_extraña = 1 if self.textura_check.isChecked() else 0
        color_extraño = 1 if self.color_check.isChecked() else 0
        empaque_extraño = 1 if self.empaque_check.isChecked() else 0
        fecha_vencimiento = self.venc_edit.date().toString("yyyy-MM-dd")
        observaciones = self.obs_edit.toPlainText()

        if not id_insumo or id_tipo is None:
            QMessageBox.warning(self, "Error", "Selecciona un insumo válido.")
            return

        success = db_helper.insertar_materias_primas(fecha, id_insumo, id_tipo, temperatura, olor_extraño, textura_extraña, color_extraño, empaque_extraño, fecha_vencimiento, observaciones)
        if success:
            QMessageBox.information(self, "Éxito", "Registro de materias primas guardado correctamente.")
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", "Error al guardar el registro.")

    def limpiar_formulario(self):
        self.fecha_edit.setDate(QtCore.QDate.currentDate())
        self.insumo_combo.setCurrentIndex(0)
        self.temp_spin.setValue(0)
        self.olor_check.setChecked(False)
        self.textura_check.setChecked(False)
        self.color_check.setChecked(False)
        self.empaque_check.setChecked(False)
        self.venc_edit.setDate(QtCore.QDate.currentDate().addDays(30))
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
    window = Ui_FormularioMateriasPrimas()
    window.show()
    sys.exit(app.exec_())
