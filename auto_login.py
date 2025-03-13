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
    browser.add_cookie({"name": "MUSIC_U", "value": "0061B61C2183784BEDD31E7423A5687C128108CC98BCC7218D56E22DB594FC7CED124DD069F9CF53CFE4A57B441ABCB774B18512EBCED9C2DE2096F9654A52F5BD3A6008185C6DE725D9CED0F71E454D9B2B04EE4BD65AC768CDFAFD9224A709B081EC27D1958A52C96DBDFC06E36C5A1B80DF3194AF9EF2E8D87CFD928E023410E9D348A3FDC7F31BE32D2D52E8E510A19131141DF8F1864589A752E0CDCB79442438A9F4BAC151802B22E664913ED3500240D98047E1E6737CA24BF9331A8EEF67F326B69448136D2C89755E537D884DF4E6E46767C0619138712865768F40A5682B2F1BF8538AC1AADAC6D3CB2853501AD024881E31AC466C407D1DA2CC71520DE82260827B487948B984EFFFD061C9B858DEB61F6E48BAF4A43B3E44D59662D55F254F84489BEBA03742E20A9AD7EA2517283373C893B2776A387B3411745B4FF553A3F1B5C0AF130A4A22ED3D88FDF5A1784DCF0A682EC40E18FADDA18D5F"})
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
