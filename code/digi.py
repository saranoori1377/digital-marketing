import requests
from bs4 import BeautifulSoup
import sqlite3

class CustomerScraper:
    def __init__(self, db_name='customers.db'):
        # اتصال به پایگاه‌داده SQL و ایجاد جدول در صورت عدم وجود
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                signup_date TEXT
            )
        ''')
        self.conn.commit()

    def scrape_customers(self, url):
        # دریافت HTML از وب‌سایت
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve data from {url}")
            return

        # پردازش HTML با BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # استخراج اطلاعات مشتری (نام، ایمیل و تاریخ ثبت‌نام)
        customers = soup.find_all('div', class_='customer-info')  # این کلاس را به کلاس واقعی تغییر دهید

        for customer in customers:
            name = customer.find('span', class_='customer-name').get_text().strip()  # کلاس و تگ مناسب را تغییر دهید
            email = customer.find('span', class_='customer-email').get_text().strip()  # کلاس و تگ مناسب را تغییر دهید
            signup_date = customer.find('span', class_='signup-date').get_text().strip()  # کلاس و تگ مناسب را تغییر دهید
            self.save_to_db(name, email, signup_date)

        print("Customer data scraping and saving completed!")

    def save_to_db(self, name, email, signup_date):
        # وارد کردن داده‌ها در پایگاه‌داده SQL
        self.c.execute('INSERT INTO customers (name, email, signup_date) VALUES (?, ?, ?)', 
                       (name, email, signup_date))
        self.conn.commit()

    def close_connection(self):
        # بستن اتصال به پایگاه‌داده
        self.conn.close()

# استفاده از کلاس برای اسکرپ اطلاعات مشتریان
if __name__ == '__main__':
    scraper = CustomerScraper()

    url = 'https://www.digikala.com'  # این URL را با URL واقعی جایگزین کنید
    scraper.scrape_customers(url)
    scraper.close_connection()
