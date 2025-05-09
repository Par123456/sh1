from datetime import datetime
import getpass
import os

def show_current_info():
    # نمایش تاریخ و زمان فعلی و نام کاربری
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    username = getpass.getuser()
    
    print(f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {formatted_time}")
    print(f"Current User's Login: {username}\n")

def decode_shell_script(file_path):
    try:
        # چک کردن وجود فایل
        if not os.path.exists(file_path):
            return f"خطا: فایل '{file_path}' پیدا نشد!"

        # خواندن محتوای فایل
        with open(file_path, 'r', encoding='utf-8') as file:
            encoded_content = file.read()

        # ذخیره متغیرها
        variables = {}
        result = ""
        
        # تقسیم محتوا به خطوط
        lines = encoded_content.split('\n')
        
        # پردازش تعریف متغیرها
        for line in lines:
            line = line.strip()
            if '=' in line and not line.startswith('eval'):
                # حذف کاراکترهای اضافی
                line = line.strip('";')
                if line:
                    try:
                        var_name, var_value = line.split('=', 1)
                        # حذف تک‌کوت‌ها از مقدار
                        var_value = var_value.strip("'")
                        variables[var_name] = var_value
                    except ValueError:
                        continue

        # پردازش دستور eval
        for line in lines:
            if line.startswith('eval'):
                # استخراج عبارت داخل eval
                eval_expr = line[5:].strip('"')
                # جداسازی متغیرها با $
                parts = eval_expr.split('$')
                
                # ترکیب مقادیر متغیرها
                for part in parts:
                    if part in variables:
                        result += variables[part]

        # ایجاد نام فایل خروجی
        output_dir = os.path.dirname(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{file_name}_decoded.sh")

        # ذخیره نتیجه در فایل جدید
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(result)

        return f"""
عملیات رمزگشایی با موفقیت انجام شد!
فایل رمزگشایی شده در مسیر زیر ذخیره شد:
{output_path}
"""

    except Exception as e:
        return f"خطا در رمزگشایی: {str(e)}"

def main():
    # نمایش اطلاعات جاری
    show_current_info()
    
    while True:
        # دریافت مسیر فایل از کاربر
        file_path = input("لطفاً مسیر کامل فایل shell را وارد کنید (یا 'exit' برای خروج): ")
        
        if file_path.lower() == 'exit':
            print("برنامه با موفقیت خاتمه یافت.")
            break
            
        # رمزگشایی و نمایش نتیجه
        result = decode_shell_script(file_path)
        print(result)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
