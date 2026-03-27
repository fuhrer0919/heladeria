# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import db_helper


class Ui_TablaMateriasPrimas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("TablaMateriasPrimas")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Tabla Control Materias Primas")

        self.setStyleSheet(
            """
            QWidget {
                background-color: #E6F3FF;
            }
            QLabel {
                color: #1A365D;
                font-size: 18px;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
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

        self.title_label = QtWidgets.QLabel("Tabla Control Materias Primas")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.layout.addSpacing(10)

        self.insumo_label = QtWidgets.QLabel("Filtrar por Insumo:")
        self.layout.addWidget(self.insumo_label)
        self.insumo_combo = QtWidgets.QComboBox()
        self.insumo_combo.addItem("Selecciona un insumo", None)
        insumos = db_helper.get_insumos_por_tipos([1, 2, 3])
        for iid, insumo in insumos:
            self.insumo_combo.addItem(insumo, iid)
        self.insumo_combo.currentIndexChanged.connect(self.cargar_datos)
        self.layout.addWidget(self.insumo_combo)

        self.layout.addSpacing(10)

        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setColumnCount(11)
        self.tabla.setHorizontalHeaderLabels(
            [
                "ID",
                "Fecha",
                "Insumo",
                "Tipo",
                "Temperatura (°C)",
                "Olor Extraño",
                "Textura Extraña",
                "Color Extraño",
                "Empaque Extraño",
                "Vencimiento",
                "Observaciones",
            ]
        )
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tabla)

        self.layout.addSpacing(10)

        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.clicked.connect(self.volver_atras)
        self.layout.addWidget(self.atras_btn)

        self.setLayout(self.layout)

    def cargar_datos(self):
        id_insumo = self.insumo_combo.currentData()
        if id_insumo is None:
            self.tabla.setRowCount(0)
            return

        registros = db_helper.get_materias_primas_por_insumo(id_insumo, limite=10)
        self.tabla.setRowCount(len(registros))
        self.tabla.clearContents()

        # Columnas binarias: Olor, Textura, Color, Empaque
        columnas_binarias = {5, 6, 7, 8}

        for row, registro in enumerate(registros):
            # Columna "Vencimiento" (índice 9) viene como "YYYY-MM-DD"
            fila_roja = False
            try:
                venc_raw = registro[9] if len(registro) > 9 else None
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

                if col in columnas_binarias:
                    if isinstance(valor, (bytes, bytearray)):
                        v_str = valor.decode("utf-8", errors="replace").strip()
                    elif valor is None:
                        v_str = ""
                    else:
                        v_str = str(valor).strip()

                    try:
                        v_int = int(v_str) if v_str != "" else 0
                        texto = "✓" if v_int == 1 else "X"
                    except ValueError:
                        texto = "✓" if v_str.lower() in {"1", "true", "t", "yes"} else "X"
                else:
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
                elif col in columnas_binarias and texto == "✓":
                    item.setBackground(QtCore.Qt.red)
                    item.setForeground(QtCore.Qt.black)
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
    window = Ui_TablaMateriasPrimas()
    window.show()
    sys.exit(app.exec_())

