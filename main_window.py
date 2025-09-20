# main_window.py
import sys
import os
import hashlib
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QInputDialog, QFileDialog, QLineEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import database
from add_dialog import AddCartridgeDialog
from bulk_dialog import AddBulkDialog
from manage_dialog import ManageDialog
from report_window import ReportWindow
import reset_db

ADMIN_PASSWORD_HASH = "3a77d5ab4c2948ada245c5d36108e3b000895712720ec4ee3d18a51085e56eef"


class MainWindow(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.setWindowTitle(f"مدیریت کارت‌ریج — ورود شده: {username}")
        self.setGeometry(100, 100, 900, 600)

        font = QFont("Tahoma", 11)
        self.setFont(font)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title = QLabel("📊 مدیریت کارت‌ریج")
        title.setFont(QFont("Tahoma", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ ثبت کارت‌ریج")
        self.btn_bulk = QPushButton("🚀 ثبت انبوه")
        self.btn_manage = QPushButton("🛠️ مدیریت بخش/ایستگاه/نوع")
        self.btn_report = QPushButton("📊 گزارش‌گیری")
        self.btn_export = QPushButton("🗑️ حذف همه داده‌ها")  # تبدیل به دکمه حذف
        self.btn_logout = QPushButton("🚪 خروج")

        for btn in [self.btn_add, self.btn_bulk, self.btn_manage, self.btn_report, self.btn_export, self.btn_logout]:
            btn.setFixedHeight(50)
            btn.setStyleSheet("padding: 8px; font-size: 14px; margin: 5px;")
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["شناسه", "بخش", "ایستگاه", "نوع", "وضعیت", "تاریخ"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.load_recent_records()

        self.btn_logout.clicked.connect(self.logout)
        self.btn_add.clicked.connect(self.open_add_dialog)
        self.btn_bulk.clicked.connect(self.open_bulk_dialog)
        self.btn_manage.clicked.connect(self.open_manage_dialog)
        self.btn_report.clicked.connect(self.open_report_dialog)

        # وصل کردن دکمه حذف دیتابیس
        try:
            self.btn_export.clicked.disconnect()
        except Exception:
            pass
        self.btn_export.clicked.connect(self.delete_database_with_password)

    def load_recent_records(self):
        try:
            records = database.get_recent_records() or []
            self.table.setRowCount(len(records))
            for row, record in enumerate(records):
                for col, value in enumerate(record):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.table.setItem(row, col, item)
        except Exception as e:
            print("Error loading recent records:", e)
            QMessageBox.warning(self, "اخطار", f"بارگذاری رکوردها موفق نبود:\n{e}")

    def logout(self):
        reply = QMessageBox.question(self, "خروج", "آیا مطمئن هستید؟", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.hide()
            from login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()

    def open_add_dialog(self):
        try:
            self.add_dialog = AddCartridgeDialog(self)
            result = self.add_dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self.load_recent_records()
        except Exception as e:
            print("Error opening AddCartridgeDialog:", e)
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن پنجره ثبت کارت‌ریج:\n{e}")

    def open_bulk_dialog(self):
        try:
            self.bulk_dialog = AddBulkDialog(self)
            result = self.bulk_dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self.load_recent_records()
        except Exception as e:
            print("Error opening AddBulkDialog:", e)
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن پنجره ثبت انبوه:\n{e}")

    def open_manage_dialog(self):
        try:
            self.manage_dialog = ManageDialog(self)
            result = self.manage_dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self.load_recent_records()
        except Exception as e:
            print("Error opening ManageDialog:", e)
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن پنجره مدیریت:\n{e}")

    def open_report_dialog(self):
        try:
            self.report_window = ReportWindow(self)
            result = self.report_window.exec()
            if result == QDialog.DialogCode.Accepted:
                self.load_recent_records()
        except Exception as e:
            print("Error opening ReportWindow:", e)
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن پنجره گزارش‌گیری:\n{e}")

    def delete_database_with_password(self):
        """
        بکاپ می‌سازد و سپس تمام جدول‌های دیتابیس را پاک می‌کند (رکوردها حذف می‌شوند).
        بر اساس reset_db.backup_db و reset_db.clear_all_tables عمل می‌کند.
        """
        try:
            # گرفتن پسورد مدیر
            pwd, ok = QInputDialog.getText(self, "تأیید مدیر", "رمز مدیر را وارد کنید:", QLineEdit.EchoMode.Password)
            if not ok:
                return

            entered_hash = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
            if entered_hash != ADMIN_PASSWORD_HASH:
                QMessageBox.warning(self, "دسترسی رد شد", "رمز عبور اشتباه است.")
                return

            # تایید نهایی از کاربر برای انجام عملیات خطرناک
            confirm = QMessageBox.question(
                self,
                "پاک‌سازی دیتابیس تست",
                "این عمل تمامی رکوردها را از تمام جدول‌ها حذف می‌کند (غیرقابل بازگشت).\nآیا می‌خواهید ادامه دهید؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return

            # 1) بکاپ خودکار
            try:
                db_path = getattr(reset_db, "DB_PATH", None) or os.path.abspath(database.DB_PATH)
                backup_path = reset_db.backup_db(db_path)
            except Exception as e:
                QMessageBox.critical(self, "خطا در بکاپ", f"بکاپ دیتابیس موفق نبود:\n{e}")
                return

            # 2) پاک‌سازی جداول
            try:
                res = reset_db.clear_all_tables(db_path)
            except Exception as e:
                QMessageBox.critical(self, "خطا در پاک‌سازی", f"پاک‌سازی دیتابیس با خطا مواجه شد:\n{e}")
                return

            # 3) نمایش نتیجه و بروزرسانی UI
            msg = f"بکاپ در: {backup_path}\n\nجداول پاک شده:\n{', '.join(res.get('tables', []))}\n\nتعداد تقریبی ردیف‌های حذف‌شده: {res.get('deleted', 0)}"
            QMessageBox.information(self, "انجام شد", msg)

            # بازخوانی جدول نمایش در پنجره اصلی
            try:
                self.load_recent_records()
            except Exception:
                pass

        except Exception as e:
            print("Unhandled error in delete_database_with_password:", e)
            QMessageBox.critical(self, "خطا", f"خطای غیرمنتظره:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    app.setFont(QFont("Tahoma", 11))
    # تست محلی با user_id=1, username='admin'
    w = MainWindow(1, "admin")
    w.show()
    sys.exit(app.exec())
