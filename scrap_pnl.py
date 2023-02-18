import datetime
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrap_pnl():
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(25)
    driver.get("https://app.quantiply.tech/auth")
    mobile_input = driver.find_element(By.NAME, "mobile")
    pass_input = driver.find_element(By.NAME, "password")
    mobile_input.send_keys("9554630599")
    pass_input.send_keys("Cherryshadowalgo@9792")
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.MuiButton-containedPrimary-210[type="submit"]')
    login_button.click()
    wait = WebDriverWait(driver, 20)
    time.sleep(30)
    button_role = driver.find_element(By.ID, "panel1d-header")
    button_role.click()
    start_time = datetime.time(9, 15)  # start time
    end_time = datetime.time(15, 30)  # end time
    table_name = f"mtm_{datetime.datetime.now().strftime('%d%m%Y')}.db"
    conn = sqlite3.connect("db_name")
    cursor = conn.cursor()
    create_table_query = f"CREATE TABLE {table_name} (time TEXT, pnl TEXT);"
    cursor.execute(create_table_query)

    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= start_time and current_time <= end_time:
            content = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "price")))
            mtm = content.find_element(By.TAG_NAME, "span")
            curr_pnl = mtm.text.split("_")[-1]
            print(curr_pnl)
            insert_table_query = f"INSERT INTO {table_name} VALUES ({current_time}, {curr_pnl})"
            cursor.execute(insert_table_query)
            time.sleep(60)
        else:
            break
    driver.quit()
    
if __name__ == "__main__":
    scrap_pnl()