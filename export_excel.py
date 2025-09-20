def export_excel(self):
    try:
        records = database.get_recent_records()
        if not records:
            QMessageBox.information(self, "اطلاع", "هیچ داده‌ای برای صادرات وجود ندارد.")
            return

        import pandas as pd
        from datetime import datetime

        df = pd.DataFrame(records, columns=["شناسه", "بخش", "ایستگاه", "نوع", "وضعیت", "تاریخ"])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"گزارش_کارت_ریج_{timestamp}.xlsx"
        df.to_excel(filename, index=False)

        full_path = os.path.abspath(filename)
        QMessageBox.information(self, "موفقیت", f"گزارش با موفقیت ذخیره شد:\n{full_path}")
    except Exception as e:
        print("Error exporting report to Excel:", e)
        QMessageBox.critical(self, "خطا", f"خطا در صادرات Excel:\n{e}")
