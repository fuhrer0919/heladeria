# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import db_helper


class Ui_TablaAseo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("TablaAseo")
        self.resize(1024, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("Tabla Control Aseo")

        self.setStyleSheet("""
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
        """)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Título
        self.title_label = QtWidgets.QLabel("Tabla Control Aseo")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.layout.addSpacing(10)

        # Filtro por elemento
        self.elemento_label = QtWidgets.QLabel("Filtrar por Elemento:")
        self.layout.addWidget(self.elemento_label)
        self.elemento_combo = QtWidgets.QComboBox()
        elementos = db_helper.get_elementos()
        self.elemento_combo.addItem("Selecciona un elemento", None)
        for eid, elemento in elementos:
            self.elemento_combo.addItem(elemento, eid)
        self.elemento_combo.currentIndexChanged.connect(self.cargar_datos)
        self.layout.addWidget(self.elemento_combo)

        self.layout.addSpacing(10)

        # Tabla
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setColumnCount(10)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Fecha", "Usuario", "Elemento", "Desinfección", "Lavado", "Barrido", "Trapeado", "Evacuación", "Observaciones"
        ])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.tabla)

        self.layout.addSpacing(10)

        # Botón Atrás
        self.atras_btn = QtWidgets.QPushButton("Atrás")
        self.atras_btn.clicked.connect(self.volver_a_admin)
        self.layout.addWidget(self.atras_btn)

        self.setLayout(self.layout)

    def cargar_datos(self):
        id_elemento = self.elemento_combo.currentData()
        if id_elemento is None:
            self.tabla.setRowCount(0)
            return

        registros = db_helper.get_aseo_por_elemento(id_elemento, limite=10)
        self.tabla.setRowCount(len(registros))
        self.tabla.clearContents()

        # Columnas: Desinfección, Lavado, Barrido, Trapeado, Evacuación
        columnas_binarias = {4, 5, 6, 7, 8}

        for row, registro in enumerate(registros):
            for col, valor in enumerate(registro):
                # Convertir valores para mostrarlos
                if col >= self.tabla.columnCount():
                    break

                if col in columnas_binarias:
                    # Mostrar 1 como check y 0 como X
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
                        # Fallback por si viniera como texto (ej: "true"/"false")
                        texto = "✓" if v_str.lower() in {"1", "true", "t", "yes"} else "X"
                else:
                    if isinstance(valor, (bytes, bytearray)):
                        texto = valor.decode("utf-8", errors="replace")
                    elif valor is None:
                        texto = ""
                    else:
                        texto = str(valor)

                item = QtWidgets.QTableWidgetItem(texto)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Solo lectura
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Centrar texto
                if col in columnas_binarias and texto == "✓":
                    item.setBackground(QtGui.QColor("#22C55E"))  # verde
                    item.setForeground(QtGui.QColor("white"))
                self.tabla.setItem(row, col, item)

    def volver_a_admin(self):
        if self.parent_window is not None:
            self.parent_window.show()
            self.close()
        else:
            self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_TablaAseo()
    window.show()
    sys.exit(app.exec_())