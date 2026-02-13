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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Navigating to login page...")
    driver.get("https://auth.projet-voltaire.fr/")
    time.sleep(5)

    print("Closing cookie banner if present...")
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(1)
    except:
        pass

    print("Checking IFrames...")
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes.")
    for i, frame in enumerate(iframes):
        print(
            f"Frame {i}: {frame.get_attribute('src')} | {frame.get_attribute('id')} | {frame.get_attribute('name')}"
        )

    print("Dumping page source related to auth_login...")
    try:
        email_input = driver.find_element(By.NAME, "auth_login")
        print(f"Email Input found: {email_input.get_attribute('outerHTML')}")
        print(f"Is Displayed: {email_input.is_displayed()}")
        print(f"Is Enabled: {email_input.is_enabled()}")
    except Exception as e:
        print(f"Email input not found: {e}")
        print("Body HTML snippet:")
        print(driver.page_source[:5000])

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
