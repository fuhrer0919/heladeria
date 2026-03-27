# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import db_helper


class Ui_FormularioCompras(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = None
        self.setupUi()

    def setupUi(self):
        self.setObjectName("FormularioCompras")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Formulario de Compras")

        # Establecer el color de fondo
        self.setStyleSheet("""
            QWidget {
                background-color: #E6F3FF;
            }
            QLabel {
                color: #1A365D;
                font-size: 18px;
            }
            QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {
                background-color: white;
                border: 2px solid #4A90E2;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4A90E2;
                border: 2px solid #2C5282;
                border-radius: 10px;
                color: white;
                padding: 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #2C5282;
            }
        """)

        # Layout principal
        layout = QtWidgets.QVBoxLayout(self)

        # Título
        title = QtWidgets.QLabel("Nueva Compra")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        # Formulario
        form_layout = QtWidgets.QFormLayout()

        # Fecha
        self.fecha_edit = QtWidgets.QDateEdit()
        self.fecha_edit.setDate(QtCore.QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        form_layout.addRow("Fecha:", self.fecha_edit)

        # Usuario
        self.usuario_combo = QtWidgets.QComboBox()
        self.cargar_usuarios()
        form_layout.addRow("Usuario:", self.usuario_combo)

        # Insumo
        self.insumo_combo = QtWidgets.QComboBox()
        self.cargar_insumos()
        form_layout.addRow("Insumo:", self.insumo_combo)

        # Valor
        self.valor_edit = QtWidgets.QLineEdit()
        self.valor_edit.setValidator(QtGui.QIntValidator(1, 999999999, self))
        self.valor_edit.setPlaceholderText("Ingrese valor")
        form_layout.addRow("Valor:", self.valor_edit)

        # Tipo de Pago
        self.tipo_pago_combo = QtWidgets.QComboBox()
        self.cargar_tipos_pago()
        form_layout.addRow("Tipo de Pago:", self.tipo_pago_combo)

        # Observaciones
        self.observaciones_edit = QtWidgets.QTextEdit()
        self.observaciones_edit.setMaximumHeight(120)
        self.observaciones_edit.textChanged.connect(self.restringir_observaciones)
        form_layout.addRow("Observaciones:", self.observaciones_edit)

        layout.addLayout(form_layout)

        # Botones Guardar y Atrás en la misma fila, centrados
        botones_layout = QtWidgets.QHBoxLayout()
        botones_layout.setSpacing(20)

        self.guardar_btn = QtWidgets.QPushButton("Guardar Compra")
        self.guardar_btn.clicked.connect(self.guardar_compra)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.clicked.connect(self.volver_a_main)

        botones_layout.addStretch()
        botones_layout.addWidget(self.guardar_btn)
        botones_layout.addWidget(self.atras_btn)
        botones_layout.addStretch()

        layout.addLayout(botones_layout)

        # Espaciador
        layout.addStretch()

    def cargar_usuarios(self):
        usuarios = db_helper.get_usuarios()
        self.usuario_combo.clear()
        ultimo_usuario = db_helper.get_ultimo_usuario_compra()
        for id_usuario, nombre in usuarios:
            self.usuario_combo.addItem(nombre, id_usuario)
            if ultimo_usuario and id_usuario == ultimo_usuario:
                self.usuario_combo.setCurrentIndex(self.usuario_combo.count() - 1)

    def cargar_insumos(self):
        insumos = db_helper.get_insumos()
        self.insumo_combo.clear()
        for id_insumo, nombre in insumos:
            self.insumo_combo.addItem(nombre, id_insumo)

    def cargar_tipos_pago(self):
        tipos = db_helper.get_tipos_de_pago()
        self.tipo_pago_combo.clear()
        for id_tipo, tipo in tipos:
            self.tipo_pago_combo.addItem(tipo, id_tipo)

    def restringir_observaciones(self):
        texto = self.observaciones_edit.toPlainText()
        if len(texto) > 100:
            self.observaciones_edit.blockSignals(True)
            self.observaciones_edit.setPlainText(texto[:100])
            cursor = self.observaciones_edit.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            self.observaciones_edit.setTextCursor(cursor)
            self.observaciones_edit.blockSignals(False)

    def guardar_compra(self):
        # Obtener valores
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        id_usuario = self.usuario_combo.currentData()
        id_insumo = self.insumo_combo.currentData()
        valor_texto = self.valor_edit.text().strip()
        if not valor_texto or not valor_texto.isdigit() or int(valor_texto) <= 0:
            QMessageBox.warning(self, "Error", "Debe ingresar el precio del insumo")
            return
        valor = int(valor_texto)
        id_tipo_pago = self.tipo_pago_combo.currentData()
        observaciones = self.observaciones_edit.toPlainText()

        # Validar que se seleccionaron usuario, insumo y tipo de pago
        if id_usuario is None or id_insumo is None or id_tipo_pago is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar usuario, insumo y tipo de pago.")
            return

        # Insertar en la base de datos
        if db_helper.insertar_compra(fecha, id_usuario, id_insumo, valor, id_tipo_pago, observaciones):
            QMessageBox.information(self, "Éxito", "Compra guardada correctamente.")
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la compra.")

    def limpiar_formulario(self):
        self.fecha_edit.setDate(QtCore.QDate.currentDate())
        self.usuario_combo.setCurrentIndex(0)
        self.insumo_combo.setCurrentIndex(0)
        self.valor_edit.setText("")
        self.tipo_pago_combo.setCurrentIndex(0)
        self.observaciones_edit.clear()

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
    window = Ui_FormularioCompras()
    window.show()
    sys.exit(app.exec_())
