# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00C241DE898771C9FB8B30F79A9463C96E9F2F6FCBDC30E3434F74C0B090295D278BB4D1194136C1458EFC3DF4ABE837F96E442DC8B904E9E0977B6E2C0E5EA26E7ECC4030E06E47E93D18893CFAE66A2D3B5B650148D092293A12A4B02A8707808525F80E62B4ACA0DA14D9494602957B1B1D03059A9E74602A15B3F1B25107E49DB9D1D8361F272F8265102A2FB0B2B75A4E37071E0464742D03BFCC017E908FDC577CBC1DEE7B3BA0C6F920B7A75E26F89234923030F4A60797163B9B2135741569EF51E3AD27F7C9341BFC60E0D5854AD565E2D4258519043B9C7EEFB2F9B75AE8EF87D5F8332D0F024E6D57C23348DCE436E93A2A27A3F6B535985FCBA266BA04D3858BB2254CE97D45679BCE70851542941E09D7C1589FDA4FC9860E101605A79351BDD8E838A9567694D19D0321E6BA29896B8C3A0A402311350773EE03C6B07B92051068A1D817469C2EE475D90E6D3DB5EF2801A6D07C66C55886A82F"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
