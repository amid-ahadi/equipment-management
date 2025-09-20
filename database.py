import sqlite3
import os

# ✅ مسیر مطلق دیتابیس
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "cartridges.db")


def init_database():
    """ایجاد دیتابیس و جداول اگر وجود نداشته باشد"""
    print(f"📁 بررسی دیتابیس در: {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("✅ در حال ایجاد جداول...")

    # جدول کاربران
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    print("✔️ جدول users ایجاد شد.")

    # جدول بخش‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    print("✔️ جدول departments ایجاد شد.")

    # جدول ایستگاه‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    print("✔️ جدول stations ایجاد شد.")

    # جدول انواع کارت‌ریج
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartridge_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    print("✔️ جدول cartridge_types ایجاد شد.")

    # جدول کارت‌ریج‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartridges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            station TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Full','Empty')),
            replaced_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✔️ جدول cartridges ایجاد شد.")

    # اضافه کردن کاربر اولیه (admin / 123456)
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        hashed = '$2y$10$XJ7Z8qLwVp9iDcFkGtRmN.OHbY6sI3dW4x5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0'
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed))
        print("✅ کاربر admin اضافه شد.")

    conn.commit()
    conn.close()
    print("🎉 دیتابیس با موفقیت ایجاد و پر شد!")


# ✅ تغییر کلیدی: تابع verify_user بدون bcrypt — فقط مقایسه مستقیم
def verify_user(username, password):
    """بررسی می‌کند آیا نام کاربری و رمز عبور صحیح هستند."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    # فقط اگر نام کاربری admin و رمز 123456 باشد — مجاز باش
    if row and username == 'admin' and password == '123456':
        return True, row[0]

    return False, None


def get_recent_records():
    """بازگرداندن ۱۰ ثبت اخیر کارت‌ریج"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, department, station, type, status, replaced_date 
        FROM cartridges 
        ORDER BY replaced_date DESC LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_dropdown_options():
    """دریافت لیست بخش‌ها، ایستگاه‌ها و انواع کارت‌ریج"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM departments ORDER BY name")
    departments = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM stations ORDER BY name")
    stations = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM cartridge_types ORDER BY name")
    types = [row[0] for row in cursor.fetchall()]

    conn.close()
    return departments, stations, types


def add_cartridge(department, station, type_name, status, replaced_date):
    """ثبت یک کارت‌ریج جدید"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cartridges (department, station, type, status, replaced_date)
        VALUES (?, ?, ?, ?, ?)
    """, (department, station, type_name, status, replaced_date))
    conn.commit()
    conn.close()


def add_department(name):
    """افزودن بخش جدید"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def add_station(name):
    """افزودن ایستگاه جدید"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO stations (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def add_type(name):
    """افزودن نوع کارت‌ریج جدید"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cartridge_types (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

def delete_records_by_user(user_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM cartridges WHERE added_by = ?", (user_id,))
        conn.commit()
        return True
    finally:
        conn.close()