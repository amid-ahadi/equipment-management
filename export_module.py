# export_module.py
import os
from datetime import datetime
import pandas as pd

def export_to_excel(records, suggested_name=None, out_path=None):
    if not records:
        raise ValueError("هیچ داده‌ای برای خروجی وجود ندارد.")
    safe_records = [[str(col) if col is not None else "" for col in row] for row in records]
    df = pd.DataFrame(safe_records, columns=["شناسه", "بخش", "ایستگاه", "نوع", "وضعیت", "تاریخ"])
    if out_path:
        file_path = out_path
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = suggested_name or f"گزارش_کارت_ریج_{ts}.xlsx"
    if not file_path.lower().endswith(".xlsx"):
        file_path += ".xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")
    return os.path.abspath(file_path)
