from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartBet AI Demo")
        self.setFixedSize(720, 1280)
        self.setWindowIcon(QtGui.QIcon("assets/logo.png"))
        self._build_ui()

    def _build_ui(self):
        # Fondo oscuro
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(30, 30, 30))
        self.setPalette(p)

        # Combo País
        self.country_cb = QtWidgets.QComboBox(self)
        self.country_cb.setGeometry(20, 20, 200, 30)
        self.country_cb.addItems(["Inglaterra", "España", "Italia"])
        # Combo Día
        self.day_cb = QtWidgets.QComboBox(self)
        self.day_cb.setGeometry(240, 20, 100, 30)
        self.day_cb.addItems(["Hoy", "Mañana"])

        # Botón recarga
        self.reload_btn = QtWidgets.QPushButton("Actualizar", self)
        self.reload_btn.setGeometry(360, 20, 100, 30)

        # Lista de partidos
        self.match_list = QtWidgets.QListWidget(self)
        self.match_list.setGeometry(20, 70, 680, 1140)
        self.match_list.setStyleSheet("""
            QListWidget { color: #EEE; background: #222; }
            QListWidget::item { padding: 10px; }
            QListWidget::item:selected { background: #444; }
        """)
