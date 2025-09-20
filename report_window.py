# report_window.py
import os
from collections import Counter
from datetime import datetime

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView, QComboBox,
    QDateEdit, QWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import database


class ReportWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 گزارش‌گیری کارت‌ریج")
        self.setGeometry(100, 100, 1100, 700)
        self.setStyleSheet("background-color: #f9f9f9;")
        font = QFont("Tahoma", 11)
        self.setFont(font)

        main_layout = QVBoxLayout(self)

        # عنوان و نوار فیلتر
        title = QLabel("📊 گزارش‌گیری کارت‌ریج")
        title.setFont(QFont("Tahoma", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        # فیلتر نوع
        filter_layout.addWidget(QLabel("نوع:"))
        self.type_filter = QComboBox()
        self.type_filter.addItem("همه")
        types = database.get_dropdown_options()[2] or []
        for t in types:
            self.type_filter.addItem(str(t))
        filter_layout.addWidget(self.type_filter)

        # فیلتر وضعیت
        filter_layout.addWidget(QLabel("وضعیت:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["همه", "Full", "Empty"])
        filter_layout.addWidget(self.status_filter)

        # فیلتر بازه تاریخ
        filter_layout.addWidget(QLabel("از تاریخ:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.setDate(QDate.currentDate().addMonths(-6))  # پیش‌فرض 6 ماه گذشته
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QLabel("تا تاریخ:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.setDate(QDate.currentDate())
        filter_layout.addWidget(self.date_to)

        # دکمه اعمال فیلتر و بازنشانی
        self.apply_btn = QPushButton("🔎 اعمال فیلتر")
        self.apply_btn.clicked.connect(self.load_report)
        filter_layout.addWidget(self.apply_btn)

        self.reset_btn = QPushButton("↺ بازنشانی")
        self.reset_btn.clicked.connect(self.reset_filters)
        filter_layout.addWidget(self.reset_btn)

        main_layout.addLayout(filter_layout)

        # ردیف اطلاعات خلاصه (تعداد کل Full / Empty)
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(20)
        self.total_label = QLabel("")  # مقداردهی در load_report
        self.total_label.setFont(QFont("Tahoma", 11, QFont.Weight.Bold))
        summary_layout.addWidget(self.total_label)
        summary_layout.addStretch()
        main_layout.addLayout(summary_layout)

        # بخش نمودارها و جدول کنار هم
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        # سمت چپ: نمودارها (دو نمودار کوچک روی هم)
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        charts_layout.setSpacing(8)

        # نمودار وضعیت (Pie) — کوچک
        self.figure_status, self.ax_status = plt.subplots(figsize=(4, 3))
        self.canvas_status = FigureCanvas(self.figure_status)
        charts_layout.addWidget(self.canvas_status)

        # نمودار نوع (Doughnut) — کوچک
        self.figure_type, self.ax_type = plt.subplots(figsize=(4, 3))
        self.canvas_type = FigureCanvas(self.figure_type)
        charts_layout.addWidget(self.canvas_type)

        content_layout.addWidget(charts_widget, 0)  # وزن کوچک برای نمودارها

        # سمت راست: جدول با فضای بیشتر
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["شناسه", "بخش", "ایستگاه", "نوع", "وضعیت", "تاریخ"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        table_layout.addWidget(self.table)

        # دکمه‌های زیر جدول
        buttons_row = QHBoxLayout()
        self.export_btn = QPushButton("📤 صادرات Excel")
        self.export_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px;")
        self.export_btn.clicked.connect(self.export_excel)
        buttons_row.addWidget(self.export_btn)

        self.save_charts_btn = QPushButton("💾 ذخیره نمودارها")
        self.save_charts_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px;")
        self.save_charts_btn.clicked.connect(self.save_charts)
        buttons_row.addWidget(self.save_charts_btn)

        buttons_row.addStretch()
        table_layout.addLayout(buttons_row)

        content_layout.addWidget(table_widget, 1)  # وزن بیشتر برای جدول

        main_layout.addLayout(content_layout)

        # دکمه بستن
        close_btn = QPushButton("❌ بستن")
        close_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 10px;")
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)

        # بارگذاری اولیه
        self.load_report()

    def reset_filters(self):
        self.type_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.date_from.setDate(QDate.currentDate().addMonths(-6))
        self.date_to.setDate(QDate.currentDate())
        self.load_report()

    def _fetch_filtered_records(self):
        # دریافت تمام رکوردها از دیتابیس و اعمال فیلترهای کاربر
        records = database.get_recent_records() or []
        filtered = []

        type_sel = self.type_filter.currentText()
        status_sel = self.status_filter.currentText()
        date_from = self.date_from.date().toString("yyyy-MM-dd")
        date_to = self.date_to.date().toString("yyyy-MM-dd")

        for r in records:
            try:
                rec_date = str(r[5])
            except Exception:
                rec_date = ""

            # فیلتر نوع
            if type_sel != "همه" and str(r[3]) != type_sel:
                continue
            # فیلتر وضعیت
            if status_sel != "همه" and str(r[4]) != status_sel:
                continue
            # فیلتر بازه تاریخ (اگر تاریخ رکورد معتبر نباشد از فیلتر رد می‌شود)
            try:
                if rec_date:
                    if rec_date < date_from or rec_date > date_to:
                        continue
            except Exception:
                continue
            filtered.append(r)
        return filtered

    def load_report(self):
        records = self._fetch_filtered_records()

        # پر یا خالی کردن جدول
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

        # نمایش تعداد کل Full و Empty
        full_count = sum(1 for r in records if str(r[4]).lower() == 'full')
        empty_count = sum(1 for r in records if str(r[4]).lower() == 'empty')
        total = len(records)
        self.total_label.setText(f"تعداد کل: {total}    پر شده: {full_count}    خالی: {empty_count}")

        # اگر هیچ رکوردی نباشد نمودارها پاک شوند
        if not records:
            self.clear_charts()
            return

        # رسم نمودار وضعیت (کوچک)
        try:
            self.ax_status.clear()
            self.ax_status.pie(
                [full_count, empty_count],
                labels=['Full', 'Empty'],
                colors=['#28a745', '#dc3545'],
                autopct='%1.1f%%'
            )
            self.ax_status.set_title("Status")
            self.canvas_status.draw()
        except Exception as e:
            print("Error plotting status chart:", e)
            self.ax_status.clear()
            self.canvas_status.draw()

        # رسم نمودار نوع (دونات) کوچک
        try:
            types = [r[3] for r in records]
            type_counts = Counter(types)
            labels = list(type_counts.keys())
            values = list(type_counts.values()) or [1]
            self.ax_type.clear()
            wedges, texts, autotexts = self.ax_type.pie(
                values, labels=labels, autopct='%1.1f%%', startangle=90
            )
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            self.figure_type.gca().add_artist(centre_circle)
            self.ax_type.set_title("Type")
            self.canvas_type.draw()
        except Exception as e:
            print("Error plotting type chart:", e)
            self.ax_type.clear()
            self.canvas_type.draw()

    def clear_charts(self):
        self.ax_status.clear()
        self.canvas_status.draw()
        self.ax_type.clear()
        self.canvas_type.draw()

    def export_excel(self):
        try:
            records = self._fetch_filtered_records() or []
            if not records:
                QMessageBox.information(self, "اطلاع", "هیچ داده‌ای برای صادرات وجود ندارد.")
                return

            # امن‌سازی داده‌ها
            safe_records = [[str(col) if col is not None else "" for col in row] for row in records]

            import pandas as pd
            from datetime import datetime
            from PyQt6.QtWidgets import QFileDialog

            suggested_name = f"گزارش_کارت_ریج_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            # نسخه ساده و سازگار با PyQt6: بدون پارامتر options
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "ذخیره گزارش Excel",
                suggested_name,
                "Excel Files (*.xlsx);;All Files (*)"
            )
            if not file_path:
                return

            if not file_path.lower().endswith(".xlsx"):
                file_path += ".xlsx"

            df = pd.DataFrame(safe_records, columns=["شناسه", "بخش", "ایستگاه", "نوع", "وضعیت", "تاریخ"])
            df.to_excel(file_path, index=False, engine="openpyxl")

            QMessageBox.information(self, "موفقیت", f"گزارش با موفقیت ذخیره شد:\n{os.path.abspath(file_path)}")
        except Exception as e:
            print("Error exporting to Excel:", e)
            QMessageBox.critical(self, "خطا", f"خطا در صادرات Excel:\n{e}")

    def save_charts(self):
        try:
            folder = QFileDialog.getExistingDirectory(self, "انتخاب پوشه برای ذخیره نمودارها")
            if not folder:
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            status_path = os.path.join(folder, f"chart_status_{timestamp}.png")
            type_path = os.path.join(folder, f"chart_type_{timestamp}.png")

            try:
                self.figure_status.savefig(status_path, bbox_inches='tight')
            except Exception as e:
                print("Failed to save status chart:", e)
            try:
                self.figure_type.savefig(type_path, bbox_inches='tight')
            except Exception as e:
                print("Failed to save type chart:", e)

            QMessageBox.information(self, "موفقیت", f"نمودارها ذخیره شد:\n{folder}")
        except Exception as e:
            print("Error saving charts:", e)
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره نمودارها:\n{e}")
