from interface import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication([])

nume = QtWidgets.QDialog()
altnume = MainWindow()
altnume.setupUi(nume)

widget = QtWidgets.QStackedWidget()
widget.addWidget(nume)
widget.setFixedHeight(715)
widget.setFixedWidth(640)
widget.show()

qp = QPalette()
qp.setColor(QPalette.ButtonText, Qt.black)
#qp.setColor(QPalette.Window, QColor(181, 255, 201))
app.setPalette(qp)

sys.exit(app.exec_())