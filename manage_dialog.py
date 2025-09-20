import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QWidget
)
from PyQt6.QtGui import QFont
import database


class ManageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🛠️ مدیریت بخش/ایستگاه/نوع")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #f9f9f9;")

        font = QFont("Tahoma", 11)
        self.setFont(font)

        layout = QVBoxLayout()

        # افزودن بخش
        layout.addWidget(QLabel("➕ افزودن بخش:"))
        self.dept_input = QLineEdit()
        self.dept_input.setPlaceholderText("نام بخش جدید...")
        layout.addWidget(self.dept_input)

        # افزودن ایستگاه
        layout.addWidget(QLabel("➕ افزودن ایستگاه:"))
        self.station_input = QLineEdit()
        self.station_input.setPlaceholderText("نام ایستگاه جدید...")
        layout.addWidget(self.station_input)

        # افزودن نوع کارت‌ریج
        layout.addWidget(QLabel("➕ افزودن نوع کارت‌ریج:"))
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("نام نوع جدید (مثال: 120 AHP)...")
        layout.addWidget(self.type_input)

        # دکمه‌ها
        btn_layout = QHBoxLayout()

        self.btn_dept = QPushButton("افزودن بخش")
        self.btn_dept.setStyleSheet("background-color: #17a2b8; color: white; padding: 8px;")
        self.btn_dept.clicked.connect(self.add_department)
        btn_layout.addWidget(self.btn_dept)

        self.btn_station = QPushButton("افزودن ایستگاه")
        self.btn_station.setStyleSheet("background-color: #17a2b8; color: white; padding: 8px;")
        self.btn_station.clicked.connect(self.add_station)
        btn_layout.addWidget(self.btn_station)

        self.btn_type = QPushButton("افزودن نوع")
        self.btn_type.setStyleSheet("background-color: #17a2b8; color: white; padding: 8px;")
        self.btn_type.clicked.connect(self.add_type)
        btn_layout.addWidget(self.btn_type)

        layout.addLayout(btn_layout)

        # دکمه لغو
        cancel_btn = QPushButton("❌ بستن")
        cancel_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 10px;")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)

    def add_department(self):
        name = self.dept_input.text().strip()
        if not name:
            QMessageBox.warning(self, "خطا", "نام بخش را وارد کنید.")
            return
        if database.add_department(name):
            QMessageBox.information(self, "موفقیت", "بخش با موفقیت اضافه شد.")
            self.dept_input.clear()
        else:
            QMessageBox.warning(self, "خطا", "این بخش قبلاً وجود دارد.")

    def add_station(self):
        name = self.station_input.text().strip()
        if not name:
            QMessageBox.warning(self, "خطا", "نام ایستگاه را وارد کنید.")
            return
        if database.add_station(name):
            QMessageBox.information(self, "موفقیت", "ایستگاه با موفقیت اضافه شد.")
            self.station_input.clear()
        else:
            QMessageBox.warning(self, "خطا", "این ایستگاه قبلاً وجود دارد.")

    def add_type(self):
        name = self.type_input.text().strip()
        if not name:
            QMessageBox.warning(self, "خطا", "نام نوع را وارد کنید.")
            return
        if database.add_type(name):
            QMessageBox.information(self, "موفقیت", "نوع کارت‌ریج با موفقیت اضافه شد.")
            self.type_input.clear()
        else:
            QMessageBox.warning(self, "خطا", "این نوع قبلاً وجود دارد.")