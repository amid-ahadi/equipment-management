import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QLineEdit, QMessageBox, QWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import database


class AddBulkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚀 ثبت انبوه کارت‌ریج")
        self.setFixedSize(500, 250)
        self.setStyleSheet("background-color: #f9f9f9;")

        font = QFont("Tahoma", 11)
        self.setFont(font)

        layout = QVBoxLayout()

        # نوع کارت‌ریج
        layout.addWidget(QLabel("نوع کارت‌ریج:"))
        self.type_combo = QComboBox()
        self.load_types()
        layout.addWidget(self.type_combo)

        # تعداد
        layout.addWidget(QLabel("تعداد:"))
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("تعداد کارت‌ریج‌های پر شده")
        self.count_input.setInputMask("9999")  # فقط 4 رقم
        self.count_input.setText("1")
        layout.addWidget(self.count_input)

        # وضعیت — فقط Full
        layout.addWidget(QLabel("وضعیت:"))
        self.status_label = QLabel("پر شده (Full)")
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        layout.addWidget(self.status_label)

        # دکمه‌ها
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("✅ ثبت انبوه")
        self.save_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px;")
        self.save_btn.clicked.connect(self.save_bulk)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("❌ لغو")
        self.cancel_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 10px;")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_types(self):
        _, _, types = database.get_dropdown_options()
        self.type_combo.clear()
        self.type_combo.addItem("-- انتخاب نوع --")
        for type_name in types:
            self.type_combo.addItem(type_name)

    def save_bulk(self):
        type_name = self.type_combo.currentText()
        count_text = self.count_input.text().strip()

        if not type_name or type_name == "-- انتخاب نوع --":
            QMessageBox.warning(self, "خطا", "لطفاً نوع کارت‌ریج را انتخاب کنید.")
            return

        if not count_text.isdigit() or int(count_text) <= 0:
            QMessageBox.warning(self, "خطا", "تعداد باید عددی مثبت باشد.")
            return

        count = int(count_text)
        status = "Full"

        # ثبت تعداد مشخص شده
        for i in range(count):
            database.add_cartridge(
                department="IT",
                station="انبار مرکزی IT",
                type_name=type_name,
                status=status,
                replaced_date="2025-01-01"  # تاریخ فرضی — برای تمایز
            )

        QMessageBox.information(self, "موفقیت", f"✅ {count} عدد کارت‌ریج {type_name} به عنوان «انبار IT» ثبت شد.")
        self.accept()