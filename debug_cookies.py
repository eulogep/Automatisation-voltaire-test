from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--start-maximized")
# options.add_argument("--headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

try:
    print("Navigating to homepage...")
    driver.get("https://www.projet-voltaire.fr/")
    time.sleep(5)

    print("Checking for cookie banner...")
    try:
        # Try ID
        btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        print(f"Found via ID: {btn.text} | Visible: {btn.is_displayed()}")
        btn.click()
        print("Clicked via ID.")
    except Exception as e:
        print(f"ID failed: {e}")
        try:
            # Try XPath
            btn = driver.find_element(
                By.XPATH, "//button[contains(., 'Accepter et fermer')]"
            )
            print(f"Found via XPath: {btn.text} | Visible: {btn.is_displayed()}")
            btn.click()
            print("Clicked via XPath.")
        except Exception as e2:
            print(f"XPath failed: {e2}")

    time.sleep(2)
    print("Checking if banner is gone on homepage...")
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler")
        print("Banner still exists in DOM (homepage).")
    except:
        print("Banner not found in DOM (homepage).")

    print("Navigating to login page...")
    driver.get("https://www.projet-voltaire.fr/connexion/")
    time.sleep(5)

    print("Checking for banner on login page...")
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler")
        print("Banner REAPPEARED on login page!")
        # Try finding a way to close it again?
    except:
        print("Banner NOT found on login page.")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
