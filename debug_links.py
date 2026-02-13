from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

try:
    print("Navigating to homepage...")
    driver.get("https://www.projet-voltaire.fr/")
    time.sleep(5)

    print("Finding 'Se connecter' links...")
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Se connecter")
    if not links:
        print("No 'Se connecter' links found.")
        # Try finding by class or other attributes if needed
        # search for any link with 'connexion' in href
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href and ("connexion" in href or "auth" in href):
                print(f"Potential Login URL: {href}")
    else:
        for link in links:
            print(f"LOGIN_URL: {link.get_attribute('href')}")

    print("Done.")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
