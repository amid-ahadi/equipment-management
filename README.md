# 🖨️ CartridgeManager — سیستم مدیریت کارت‌ریج چاپگر (ویندوز دسکتاپ)

> یک نرم‌افزار **حروفه‌ای و بدون نیاز به اینترنت** برای مدیریت موجودی کارت‌ریج در کارگاه‌های تعمیرات، دفترها و بیمارستان‌ها — با گزارش‌گیری، ثبت انبوه و صادرات Excel.


---

## ✅ ویژگی‌های کلیدی

| ویژگی | توضیح |
|-------|--------|
| 🔐 **احراز هویت ایمن** | ورود با نام کاربری `admin` و رمز `123456` — با CAPTCHA جلوی ربات‌ها |
| 📥 **ثبت انبوه کارت‌ریج** | یک کلیک — ۱۰ تا کارت‌ریج پر شده ثبت شوند — بدون نیاز به تکرار |
| 🛠️ **مدیریت بخش/ایستگاه/نوع** | افزودن بخش، ایستگاه یا نوع کارت‌ریج جدید — بدون نیاز به دیتابیس دستی |
| 📊 **گزارش‌گیری هوشمند** | نمودارهای Pie, Bar و Doughnut برای تحلیل وضعیت و نوع کارت‌ریج |
| 📤 **صادرات به Excel** | دانلود فایل `.xlsx` با تمام رکوردها — برای گزارش‌های اداری |
| 💾 **دیتابیس محلی (SQLite)** | همه داده‌ها در یک فایل `cartridges.db` ذخیره می‌شوند — بدون نیاز به سرور |
| 🖥️ **نسخه دسکتاپ ویندوزی (.exe)** | فقط کلیک کنید — نیازی به نصب پایتون، مرورگر یا سرور نیست |
| 🌐 **پشتیبانی کامل از فارسی و RTL** | تمام رابط کاربری، دکمه‌ها و گزارش‌ها به صورت راست به چپ |
| 🚫 **بدون اینترنت** | کاملاً لوکال — ایده‌آل برای محیط‌های حساس و اداری |

---


## 🔐 ورود به سیستم

- **نام کاربری:** `admin`  
- **رمز عبور:** `123456`  
- **کد CAPTCHA:** عدد نمایش داده شده را وارد کنید

> 💡 بعد از ورود، می‌توانید رمز عبور را در بخش **"تغییر رمز عبور"** تغییر دهید.

---

## 📈 قابلیت‌های اصلی

| دکمه | عملکرد |
|------|--------|
| ➕ **ثبت کارت‌ریج** | ثبت یک کارت‌ریج با انتخاب بخش، ایستگاه، نوع و وضعیت |
| 🚀 **ثبت انبوه** | ثبت ۱۰ تا کارت‌ریج با یک کلیک (مثلاً ۱۰ تا `120 AHP` پر شده) |
| 🛠️ **مدیریت بخش/ایستگاه/نوع** | افزودن بخش، ایستگاه یا نوع کارت‌ریج جدید |
| 📊 **گزارش‌گیری** | نمودارهای وضعیت، ماهانه و نوع کارت‌ریج با تحلیل تصویری |
| 📤 **صادرات Excel** | دانلود فایل `گزارش_کارت_ریج.xlsx` با تمام رکوردها |
| 🚪 **خروج** | خروج از سیستم و بازگشت به صفحه ورود |

---

## 🛠️ فناوری‌های استفاده شده

| بخش | تکنولوژی |
|------|----------|
| رابط کاربری | PyQt6 (Python GUI) |
| دیتابیس | SQLite3 (فایل `.db`) |
| نمودارها | Matplotlib |
| صادرات Excel | Pandas + OpenPyXL |
| بسته‌بندی به .exe | PyInstaller |
| زبان | فارسی — پشتیبانی کامل RTL |
| امنیت | password_hash (هش با bcrypt) + CAPTCHA |

---


## 📜 مجوز

MIT License

Copyright (c) 2025 Amid Ahadi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

## 👥 نویسنده

> **توسعه‌دهنده:** عميد احدي | Amid Ahadi
> **موقعیت:** ایران 🇮🇷  
> **تماس:** amid-ahadi.ir  

> _"دیگه نیازی به اکسل و دفترچه نیست — فقط کلیک کن، ثبت کن، گزارش بگیر."_

---

## 📌 نکته مهم

> ❗ این نرم‌افزار **فقط برای استفاده لوکال و داخلی** طراحی شده است.  
> اگر قصد دارید آن را روی اینترنت منتشر کنید — حتماً از **HTTPS و احراز هویت پیشرفته** استفاده کنید.
