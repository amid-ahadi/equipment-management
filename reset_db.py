# reset_db.py
import os
import shutil
import sqlite3
from datetime import datetime

# مسیر فایل sqlite پروژه را در اینجا قرار بده یا از database.DB_PATH استفاده کن
DB_PATH = "data/cartridges.db"   # اگر در ماژول database تعریف شده، از آن مقدار استفاده کن

def backup_db(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")
    base = os.path.splitext(os.path.basename(db_path))[0]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{base}_backup_{ts}.db"
    backup_path = os.path.join(os.path.dirname(os.path.abspath(db_path)), backup_name)
    shutil.copy2(db_path, backup_path)
    return backup_path

def get_user_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    rows = cur.fetchall()
    return [r[0] for r in rows]

def clear_all_tables(db_path):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        # غیرفعال کردن foreign keys برای حذف ساده
        cur.execute("PRAGMA foreign_keys = OFF;")
        conn.commit()

        tables = get_user_tables(conn)
        if not tables:
            return {"deleted": 0, "tables": []}

        total_deleted = 0
        # اجرای حذف در یک تراکنش واحد
        conn.execute("BEGIN;")
        try:
            for t in tables:
                # اگر می‌خواهی بعضی جدول‌ها را نگه داری کن، فیلتر کن این لیست را
                cur.execute(f"DELETE FROM \"{t}\";")
                cnt = cur.rowcount
                total_deleted += cnt if cnt is not None else 0
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            # بازگرداندن foreign keys
            cur.execute("PRAGMA foreign_keys = ON;")
            conn.commit()

        return {"deleted": total_deleted, "tables": tables}
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        print("Backing up database...")
        backup_path = backup_db(DB_PATH)
        print("Backup created at:", backup_path)

        print("Clearing all user tables in database...")
        res = clear_all_tables(DB_PATH)
        print(f"Cleared tables: {res['tables']}")
        print(f"Total rows deleted (approx): {res['deleted']}")

        print("Done. Database is now empty (tables remain).")
        print("If you want to recreate schema from a SQL file, place schema.sql and I can provide the command.")
    except Exception as e:
        print("Error:", e)
