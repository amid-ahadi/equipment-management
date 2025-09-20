import sys
from PyQt6.QtWidgets import QApplication
from login_window import LoginWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

app = QApplication(sys.argv)
app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
app.setFont(QFont("Tahoma", 11))
