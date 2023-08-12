""" import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)"""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import webbrowser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from seleniumwire import webdriver
import time
from fake_useragent import UserAgent

base_url = "https://www.amazon.com/dp/"

def set_tite_log():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(credentials)
        log_sheet = client.open("Glue_ASIN").worksheet("time_log")
        current_dateTime = str(datetime.now())[:19]
        row_number = len(log_sheet.get_all_values()) + 1

        # Додавання часу остатньої перевірки
        log_sheet.update_cell(row_number, 1, current_dateTime)
    except:
        pass

def final_massage (bad_asin):
    if bad_asin == 0:
        return "Все добре. Перевірка завершена."
    else:
        return "Перевірка завершена."

def get_element_text(driver, locator, attribute=None):
    element = driver.find_element(*locator)
    if attribute:
        return element.get_attribute(attribute)
    return element.text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привіт! \nДля перевірки асінів введіть /check_asins")

def fetch_asins_from_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(credentials)
        sheet = client.open("Glue_ASIN").worksheet("skleyka")
        review = sheet.col_values(2)[1:6]
        short_title = sheet.col_values(3)[1:6]
        parent_SKU = sheet.col_values(4)[1:6]
        AS = sheet.col_values(5)[1:6]
        return [AS, review, parent_SKU, short_title]
    except Exception as e:
        print("Error", f"Помилка при імпорті ASINs from Google Sheets: {e}")

def set_new_review(index, review):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(credentials)
        new_review = client.open("Glue_ASIN").worksheet("skleyka")
        row_number = index + 2

        # Додавання часу остатньої перевірки
        new_review.update_cell(row_number, 2, review)
    except:
        pass  

async def check_asins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    AS, old_review, parent_SKU, short_title = fetch_asins_from_google_sheets()

    # Ініціалізація драйвера браузера для збереження сторінки
    chrome_options = Options()
    useragent = UserAgent()
    proxy_options = {
        'proxy': {
            'http': 'http://r7pW3ms3:EQ6cdt9E@217.198.182.159:61464',
            'https': 'http://r7pW3ms3:EQ6cdt9E@217.198.182.159:61464'
        }
    }
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver_save = webdriver.Chrome(
        options=chrome_options,
        seleniumwire_options=proxy_options
    )
    # driver_save = webdriver.Chrome(options=chrome_options)

    #!!!
    bad_asin = 0
    set_tite_log()
    await update.effective_message.reply_text("Перевірка почалась")
    for index in range(len(AS)):
        asin = AS[index]
        Old_Review = int(old_review[index])
        amazon_url = base_url + asin
        try:
            driver_save.get(amazon_url)
        except Exception as e:
            print(e)
        title, rating, reivew, brand = "", 0, 0, ""
        try:
            title_locator = (By.ID, "productTitle")
            title = get_element_text(driver_save, title_locator)
        except:
            title = "N/A"
        try:    
            reivew_locator = (By.ID, "acrCustomerReviewText")
            reivew = int(get_element_text(driver_save, reivew_locator).split()[0].replace(",", ""))
        except:
            reivew = 0
        try:
            stars_locator = (By.ID, "acrPopover")
            rating = float(get_element_text(driver_save, stars_locator).split()[0])
        except:
            rating = 0
        try:
            img_locator = (By.ID, "landingImage")
            img = get_element_text(driver_save, img_locator, "src")
        except:
            img = "N/A"
        try:
            brand_locator = (By.XPATH, "//a[@id='bylineInfo']")
            brand_element = driver_save.find_element(*brand_locator)
            brand_text = brand_element.text
            brand_match = re.search(r'Visit the (.*) Store', brand_text) if brand_text.startswith("Visit the ") else re.search(r"Brand:\s*(.*)", brand_text)
            if brand_match:
                brand = brand_match.group(1)
        except:
            brand = "Reivew неможливо знайти"
        
        if title == "N/A":
            bad_asin += 1
            await update.effective_message.reply_text(f"""{amazon_url}\n{short_title[index]}\nAsin {asin} неможливо знайти""")
        elif Old_Review < reivew:
            await update.effective_message.reply_text(f"""Назва: {title}""")
            set_new_review(index, reivew)
        elif Old_Review > reivew:
            bad_asin += 1
            await update.effective_message.reply_text(f"""{amazon_url}\nParent SKU: {parent_SKU[index]} \nAsin: {asin}\nНазва: {title[0:15]}\nКоротка назва: {short_title[index]}\nБренд: {brand}\nРейтинг: {rating}\nВідгуки: {reivew}({reivew - Old_Review})\n{img}""", )
        else:
            await update.effective_message.reply_text(f"""Назва: {title}""")

    await update.effective_message.reply_text(final_massage(bad_asin))
        
        

application = Application.builder().token("6049177154:AAESqApBV7VKR-sejc0ThVrG7xWG5PWIIbM").build()

application.add_handler(CommandHandler(["start", "help"], start))
application.add_handler(CommandHandler("check_asins", check_asins))

# application.add_handler(CommandHandler("check_asins_input", check_asins_input))

application.run_polling(allowed_updates=Update.ALL_TYPES)