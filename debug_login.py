from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

EMAIL = "mabiala@et.esiea.fr"
PASSWORD = "Jesusestseigneur2024*"

print("Starting debug script...")

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

print("Initializing driver...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Navigating to homepage...")
    driver.get("https://www.projet-voltaire.fr/")

    # Cookie
    print("Handling cookies...")
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_btn.click()
        print("Cookie: Accepted via ID.")
    except:
        try:
            cookie_btn = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Accepter et fermer')]"
            )
            cookie_btn.click()
            print("Cookie: Accepted via Text.")
        except:
            print("Cookie: No banner found.")

    # Login Nav
    print("Navigating to login...")
    try:
        login_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Se connecter"))
        )
        login_link.click()
        print("Login link clicked.")
    except:
        driver.get("https://auth.projet-voltaire.fr/")
        print("Direct nav to auth.")

    # Form
    print("Filling email...")
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "auth_login"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("Email filled.")

    print("Filling password...")
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "auth_password"))
        )
        print("Password input found by name.")
    except:
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[type='password']")
            )
        )
        print("Password input found by type.")

    password_input.clear()
    password_input.send_keys((PASSWORD))
    print("Password filled.")

    # Submit
    print("Submitting...")
    try:
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "auth_header_submit"))
        )
        submit_btn.click()
        print("Submit button clicked.")
    except:
        password_input.submit()
        print("Form submitted via input.")

    # Check
    print("Waiting for dashboard...")
    WebDriverWait(driver, 20).until(EC.url_contains("tableau-de-bord"))
    print("SUCCESS: Logged in!")

except Exception as e:
    print(f"FAILURE: {e}")
    driver.save_screenshot("debug_failure.png")
finally:
    driver.quit()
    print("Driver closed.")
