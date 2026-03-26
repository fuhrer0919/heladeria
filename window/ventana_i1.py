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
        self.title_label = QtWidgets.QLabel("Formulario de Control Materias Primas")
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

        # Insumo
        self.insumo_label = QtWidgets.QLabel("Insumo:")
        self.layout.addWidget(self.insumo_label)
        self.insumo_combo = QtWidgets.QComboBox()
        insumos = db_helper.get_insumos_filtrados()
        for iid, insumo in insumos:
            self.insumo_combo.addItem(insumo, iid)
        self.layout.addWidget(self.insumo_combo)

        self.layout.addSpacing(10)

        # Temperatura
        self.temp_label = QtWidgets.QLabel("Temperatura (°C):")
        self.layout.addWidget(self.temp_label)
        self.temp_spin = QtWidgets.QSpinBox()
        self.temp_spin.setRange(-50, 100)  # Rango razonable
        self.layout.addWidget(self.temp_spin)

        self.layout.addSpacing(20)

        # Anomalías
        self.anomalias_label = QtWidgets.QLabel("Anomalías detectadas:")
        self.layout.addWidget(self.anomalias_label)

        self.olor_check = QtWidgets.QCheckBox("Olor Extraño")
        self.layout.addWidget(self.olor_check)

        self.textura_check = QtWidgets.QCheckBox("Textura Extraña")
        self.layout.addWidget(self.textura_check)

        self.color_check = QtWidgets.QCheckBox("Color Extraño")
        self.layout.addWidget(self.color_check)

        self.empaque_check = QtWidgets.QCheckBox("Empaque Extraño")
        self.layout.addWidget(self.empaque_check)

        self.layout.addSpacing(10)

        # Fecha Vencimiento
        self.venc_label = QtWidgets.QLabel("Fecha de Vencimiento:")
        self.layout.addWidget(self.venc_label)
        self.venc_edit = QtWidgets.QDateEdit()
        self.venc_edit.setDate(QtCore.QDate.currentDate().addDays(30))  # Default +30 días
        self.venc_edit.setCalendarPopup(True)
        self.layout.addWidget(self.venc_edit)

        self.layout.addSpacing(10)

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
        self.guardar_btn.clicked.connect(self.guardar_materias)
        self.button_layout.addWidget(self.guardar_btn)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.clicked.connect(self.volver_a_f1)
        self.button_layout.addWidget(self.atras_btn)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

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
