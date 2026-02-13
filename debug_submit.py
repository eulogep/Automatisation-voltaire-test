"""
Script de débogage pour tester la soumission du formulaire et observer le résultat
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Credentials
EMAIL = "mabiala@et.esiea.fr"
PASSWORD = "Jesusestseigneur2024*"

def human_type(element, text):
    """Simule une frappe humaine"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

def force_clear_cookies(driver):
    """Supprime radicalement toute trace de bannière de cookies"""
    print("🧹 Nettoyage des cookies...")
    
    for attempt in range(3):
        try:
            cookie_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
            print(f"✅ Cookies cliqués (tentative {attempt + 1})")
            time.sleep(1)
            
            try:
                WebDriverWait(driver, 2).until(
                    EC.invisibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))
                )
                print("✅ Bannière disparue")
                break
            except Exception:
                print("⚠️ Bannière toujours là...")
                continue
        except Exception:
            if attempt == 0:
                print("ℹ️ Pas de cookies")
            break
    
    # Nettoyage DOM
    driver.execute_script("""
        ['onetrust-banner-sdk', 'onetrust-consent-sdk', 'ot-sdk-btn-floating'].forEach(id => {
            var el = document.getElementById(id);
            if (el) el.remove();
        });
        document.body.style.overflow = 'auto';
        document.body.style.pointerEvents = 'auto';
    """)
    time.sleep(0.5)

# Configuration
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    wait = WebDriverWait(driver, 15)
    
    # 1. Homepage
    print("📍 Homepage...")
    driver.get("https://www.projet-voltaire.fr/")
    force_clear_cookies(driver)
    
    # 2. Clic "Se connecter"
    print("🔗 Clic 'Se connecter'...")
    login_btn = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Se connecter")))
    login_btn.click()
    time.sleep(2)
    
    # 3. Cookies page login
    force_clear_cookies(driver)
    
    # 4. Remplir formulaire
    print(f"📍 URL: {driver.current_url}")
    print("✍️ Remplissage...")
    
    email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Identifiant'], input[name='auth_login'], input[type='email']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", email_input)
    email_input.clear()
    human_type(email_input, EMAIL)
    
    pass_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Mot de passe'], input[name='auth_password'], input[type='password']")
    human_type(pass_input, PASSWORD)
    
    print("📸 Screenshot avant submit...")
    driver.save_screenshot("screenshots/debug_before_submit.png")
    
    # 5. Submit
    print("🚀 Submit...")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    try:
        submit_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", submit_btn)
    
    # 6. Attendre et observer
    print("⏳ Attente de 10 secondes...")
    time.sleep(10)
    
    print(f"\n📍 URL APRÈS SUBMIT: {driver.current_url}")
    print(f"📄 TITRE: {driver.title}")
    
    # 7. Screenshot post-submit
    driver.save_screenshot("screenshots/debug_after_submit.png")
    print("📸 Screenshot après submit sauvegardé")
    
    # 8. Vérifier si erreur de login
    try:
        error_msg = driver.find_element(By.CSS_SELECTOR, ".error, .alert, [class*='error'], [class*='alert']")
        print(f"❌ MESSAGE D'ERREUR TROUVÉ: {error_msg.text}")
    except Exception:
        print("✅ Pas de message d'erreur visible")
    
    # 9. Pause pour inspection
    print("\n⏸️  Pause de 15 secondes pour inspection manuelle...")
    time.sleep(15)
    
finally:
    driver.quit()
    print("\n✅ Navigateur fermé")
