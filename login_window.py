import sys
import random
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont
import database
from main_window import MainWindow
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ورود به سیستم")
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        font = QFont("Tahoma", 11)
        self.setFont(font)

        self.captcha_text = str(random.randint(1000, 9999))
        self.captcha_image_path = "captcha.png"
        self.generate_captcha()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel("🔒")
        logo_label.setFont(QFont("Arial", 40))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        title = QLabel("ورود به سیستم")
        title.setFont(QFont("Tahoma", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("نام کاربری:"), 0, 0)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("نام کاربری")
        form_layout.addWidget(self.username_input, 0, 1)

        form_layout.addWidget(QLabel("رمز عبور:"), 1, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("رمز عبور")
        form_layout.addWidget(self.password_input, 1, 1)

        form_layout.addWidget(QLabel("کد امنیتی:"), 2, 0)
        captcha_layout = QHBoxLayout()
        self.captcha_label = QLabel()
        self.captcha_label.setPixmap(QPixmap(self.captcha_image_path))
        self.captcha_label.setFixedSize(120, 50)
        self.captcha_label.setStyleSheet("border: 1px solid #ccc; background: white;")
        captcha_layout.addWidget(self.captcha_label)

        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("کد را وارد کنید")
        self.captcha_input.setMaxLength(4)
        self.captcha_input.setFixedWidth(80)
        captcha_layout.addWidget(self.captcha_input)

        form_layout.addLayout(captcha_layout, 2, 1)

        change_btn = QPushButton("تغییر کد")
        change_btn.clicked.connect(self.refresh_captcha)
        change_btn.setFixedWidth(80)
        form_layout.addWidget(change_btn, 2, 2)

        layout.addLayout(form_layout)

        self.login_btn = QPushButton("ورود")
        self.login_btn.setStyleSheet("background-color: #007bff; color: white; padding: 10px; border-radius: 5px;")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

    def generate_captcha(self):
        img = Image.new('RGB', (120, 50), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((20, 5), self.captcha_text, fill=(0, 0, 0), font=font)
        img.save(self.captcha_image_path)

    def refresh_captcha(self):
        self.captcha_text = str(random.randint(1000, 9999))
        self.generate_captcha()
        self.captcha_label.setPixmap(QPixmap(self.captcha_image_path))
        self.captcha_input.clear()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        captcha = self.captcha_input.text().strip()

        if not username or not password or not captcha:
            QMessageBox.warning(self, "خطا", "لطفاً همه فیلدها را پر کنید.")
            return

        if captcha != self.captcha_text:
            QMessageBox.warning(self, "خطا", "کد امنیتی اشتباه است.")
            self.refresh_captcha()
            return

        # ✅ فقط این شرط — بدون هیچ ارتباطی با دیتابیس یا bcrypt
        if username == 'admin' and password == '123456':
            QMessageBox.information(self, "موفقیت", f"ورود موفق! خوش آمدید، {username}")
            self.main_window = MainWindow(1, username)  # ← اینجا
            self.main_window.show()
            self.hide()  # ← اینجا
        else:
            QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور اشتباه است.")
            self.refresh_captcha()