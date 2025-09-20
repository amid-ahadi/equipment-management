import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QDateEdit, QMessageBox, QWidget
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
import database


class AddCartridgeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("➕ ثبت کارت‌ریج")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: #f9f9f9;")

        font = QFont("Tahoma", 11)
        self.setFont(font)

        layout = QVBoxLayout()

        # بخش
        layout.addWidget(QLabel("بخش:"))
        self.department_combo = QComboBox()
        self.load_departments()
        layout.addWidget(self.department_combo)

        # ایستگاه
        layout.addWidget(QLabel("ایستگاه:"))
        self.station_combo = QComboBox()
        self.load_stations()
        layout.addWidget(self.station_combo)

        # نوع کارت‌ریج
        layout.addWidget(QLabel("نوع کارت‌ریج:"))
        self.type_combo = QComboBox()
        self.load_types()
        layout.addWidget(self.type_combo)

        # وضعیت
        layout.addWidget(QLabel("وضعیت:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["", "Full", "Empty"])
        self.status_combo.setCurrentIndex(0)
        layout.addWidget(self.status_combo)

        # تاریخ تعویض
        layout.addWidget(QLabel("تاریخ تعویض (میلادی):"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setMaximumDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        # دکمه‌ها
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("✅ ثبت")
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.save_btn.clicked.connect(self.save_cartridge)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("❌ لغو")
        self.cancel_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 10px;")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_departments(self):
        departments, _, _ = database.get_dropdown_options()
        self.department_combo.clear()
        self.department_combo.addItem("-- انتخاب بخش --")
        for dept in departments:
            self.department_combo.addItem(dept)

    def load_stations(self):
        _, stations, _ = database.get_dropdown_options()
        self.station_combo.clear()
        self.station_combo.addItem("-- انتخاب ایستگاه --")
        for station in stations:
            self.station_combo.addItem(station)

    def load_types(self):
        _, _, types = database.get_dropdown_options()
        self.type_combo.clear()
        self.type_combo.addItem("-- انتخاب نوع --")
        for type_name in types:
            self.type_combo.addItem(type_name)

    def save_cartridge(self):
        department = self.department_combo.currentText()
        station = self.station_combo.currentText()
        type_name = self.type_combo.currentText()
        status = self.status_combo.currentText()
        replaced_date = self.date_edit.date().toString("yyyy-MM-dd")

        if not all([department != "-- انتخاب بخش --",
                    station != "-- انتخاب ایستگاه --",
                    type_name != "-- انتخاب نوع --",
                    status != ""]):
            QMessageBox.warning(self, "خطا", "لطفاً همه فیلدها را به درستی پر کنید.")
            return

        database.add_cartridge(department, station, type_name, status, replaced_date)
        QMessageBox.information(self, "موفقیت", "کارت‌ریج با موفقیت ثبت شد.")
        self.accept()  # بستن پنجره با موفقیت

