# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import db_helper


class Ui_TablaVencimientos(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()
        self.cargar_datos()

    def setupUi(self):
        self.setObjectName("TablaVencimientos")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Tabla Vencimientos Próximos")

        self.setStyleSheet(
            """
            QWidget {
                background-color: #E6F3FF;
            }
            QLabel {
                color: #1A365D;
                font-size: 18px;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #4A90E2;
                border-radius: 5px;
                gridline-color: #E6F3FF;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4A90E2;
                color: white;
            }
            QHeaderView::section {
                background-color: #4A90E2;
                color: white;
                padding: 5px;
                border: 1px solid #2C5282;
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
            """
        )

        self.layout = QtWidgets.QVBoxLayout(self)

        self.title_label = QtWidgets.QLabel("Vencimientos menores a 2 meses")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.layout.addSpacing(10)

        # Tabla
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(
            [
                "ID",
                "Fecha",
                "Insumo",
                "Tipo",
                "Temperatura (°C)",
                "Vencimiento",
                "Observaciones",
            ]
        )
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tabla)

        self.layout.addSpacing(10)

        # Botones
        self.button_layout = QtWidgets.QHBoxLayout()

        self.actualizar_btn = QtWidgets.QPushButton("Actualizar")
        self.actualizar_btn.clicked.connect(self.cargar_datos)
        self.button_layout.addWidget(self.actualizar_btn)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.clicked.connect(self.volver_atras)
        self.button_layout.addWidget(self.atras_btn)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def cargar_datos(self):
        # 2 meses ~= 60 días, críticos: 15 días
        registros = db_helper.get_materias_primas_vencimiento_proximo(dias=60, dias_criticos=15, limite=500)
        self.tabla.setRowCount(len(registros))
        self.tabla.clearContents()

        for row, registro in enumerate(registros):
            # Columna "Vencimiento" (índice 5)
            fila_roja = False
            try:
                venc_raw = registro[5] if len(registro) > 5 else None
                venc_str = ""
                if isinstance(venc_raw, (bytes, bytearray)):
                    venc_str = venc_raw.decode("utf-8", errors="replace").strip()
                elif venc_raw is not None:
                    venc_str = str(venc_raw).strip()

                if venc_str:
                    fecha_venc = QtCore.QDate.fromString(venc_str, "yyyy-MM-dd")
                    if fecha_venc.isValid():
                        hoy = QtCore.QDate.currentDate()
                        if fecha_venc <= hoy.addDays(15):
                            fila_roja = True
            except Exception:
                fila_roja = False

            for col, valor in enumerate(registro):
                if col >= self.tabla.columnCount():
                    break

                if isinstance(valor, (bytes, bytearray)):
                    texto = valor.decode("utf-8", errors="replace")
                elif valor is None:
                    texto = ""
                else:
                    texto = str(valor)

                item = QtWidgets.QTableWidgetItem(texto)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if fila_roja:
                    item.setBackground(QtCore.Qt.red)
                    item.setForeground(QtCore.Qt.white)
                self.tabla.setItem(row, col, item)

    def volver_atras(self):
        if self.parent_window is not None:
            self.parent_window.show()
            self.close()
        else:
            self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Ui_TablaVencimientos()
    window.show()
    sys.exit(app.exec_())

