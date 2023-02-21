from __future__ import annotations
from common import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def convert_time_to_seconds(time_string: str) -> int:
    """Convert given time string to seconds
        Args:
            time_string (str): time string (60s, 1m, 1h)
    """
    time_unit = time_string[-1]  # extract the time unit (s, m, h)
    time_value = int(time_string[:-1])  # extract the time value (integer)
    if time_unit == 's':
        return time_value
    elif time_unit == 'm':
        return time_value * 60
    elif time_unit == 'h':
        return time_value * 60 * 60
    else:
        raise ValueError("Invalid time unit: {}".format(time_unit))

def scrap_pnl(args: dict[str, typing.Any]):
    """Scrap quantiply page and writes mtm to given file
        Args:
            args (dict[str, typing.Any]): command line arguments
    """
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    options = Options()
    logging.info("Start Web browser in headless mode")
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(25)
    logging.info("Load Quantiply in browser")
    driver.get("https://app.quantiply.tech/auth")
    mobile_input = driver.find_element(By.NAME, "mobile")
    pass_input = driver.find_element(By.NAME, "password")
    mobile_input.send_keys(args.get("phone"))
    pass_input.send_keys(args.get("password"))
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.MuiButton-containedPrimary-210[type="submit"]')
    login_button.click()
    wait = WebDriverWait(driver, 20)
    time.sleep(30)
    logging.info("Logged in successfully to Quantiply")
    button_role = driver.find_element(By.ID, "panel1d-header")
    button_role.click()
    time_interval = convert_time_to_seconds(args.get("interval"))
    start_time = datetime.time(9, 15)
    end_time = datetime.time(15, 30)
    # Get current program directory
    program_dir = os.getcwd() 
    mtm_outfile = os.path.join(program_dir, f"mtm_{datetime.datetime.now().strftime('%Y%m%d')}.csv")
    if args.get("outfile"):
        mtm_outfile = args.get("outfile")
    # Open the file in write mode to clear its contents
    with open(mtm_outfile, 'w') as file:
        pass 
    with open(mtm_outfile, 'a', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(["datetime", "pnl"])
        while True:
            current_time = datetime.datetime.now().time()
            if current_time >= start_time and current_time <= end_time:
                content = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "price")))
                mtm = content.find_element(By.TAG_NAME, "span")
                curr_pnl = mtm.text.split("_")[-1].replace("₹", "").replace(",", "")
                writer.writerow([current_time, curr_pnl])
                time.sleep(time_interval) 
            else:
                break
    logging.info(f"Day's MTM stored at: {mtm_outfile}")
    driver.quit()

def parse_cmds() -> dict[str, typing.Any]:
    """Parses command line
        Returns:
            dict[str, typing.Any]: parsed arguments
    """
    parser = argparse.ArgumentParser(description="Scrap Day MTM from Quantiply")
    parser.add_argument("-outfile", type=str, help="CSV file to store days MTM")
    parser.add_argument("-interval", type=str, default="60s",
                        help="MTM check time interval (Default: 60s, Format:60s, 1m, 1h)")
    parser.add_argument("-phone", type=str, required=True, help="Quantiply Login Phone number")
    parser.add_argument("-password", type=str, required=True, help="Quantiply Login Password")
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = parse_cmds()
    logging.basicConfig(level=logging.INFO)
    scrap_pnl(args)