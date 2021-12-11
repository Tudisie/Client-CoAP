from interface import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
app = QApplication([])

qp = QPalette()
qp.setColor(QPalette.ButtonText, Qt.black)
qp.setColor(QPalette.Window, QColor(194, 217, 255))
#qp.setColor(QPalette.Button, QColor(0, 179, 255))
app.setPalette(qp)

windows = MainWindow()
sys.exit(app.exec_())