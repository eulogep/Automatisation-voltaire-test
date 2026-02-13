from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

try:
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print("Installing ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    print(f"Driver installed at: {service.path}")

    print("Initializing WebDriver...")
    driver = webdriver.Chrome(service=service, options=options)

    print("Navigating to google.com...")
    driver.get("https://www.google.com")
    print("Title:", driver.title)

    driver.quit()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
