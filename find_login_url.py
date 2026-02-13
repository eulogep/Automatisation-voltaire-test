"""
Script de débogage pour identifier l'URL correcte de connexion
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    print("📍 Accès à la homepage...")
    driver.get("https://www.projet-voltaire.fr/")
    time.sleep(2)
    
    # 2. Accepter cookies
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_btn.click()
        print("✅ Cookies acceptés")
        time.sleep(1)
    except Exception:
        print("ℹ️ Pas de cookies")
    
    # 3. Cliquer sur "Se connecter"
    print("🔗 Clic sur 'Se connecter'...")
    login_btn = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Se connecter")))
    login_btn.click()
    
    # 4. Attendre la redirection
    time.sleep(3)
    
    # 5. Afficher l'URL finale
    print(f"\n🎯 URL DE CONNEXION TROUVÉE : {driver.current_url}\n")
    
    # 6. Vérifier la présence du formulaire
    try:
        email_field = driver.find_element(By.NAME, "auth_login")
        print("✅ Formulaire de connexion trouvé !")
        print(f"   - Champ email : {email_field.get_attribute('name')}")
        
        pass_field = driver.find_element(By.NAME, "auth_password")
        print(f"   - Champ password : {pass_field.get_attribute('name')}")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        print(f"   - Bouton submit : {submit_btn.text}")
        
    except Exception as e:
        print(f"❌ Formulaire non trouvé : {e}")
    
    # 7. Screenshot
    driver.save_screenshot("screenshots/debug_real_login_url.png")
    print("\n📸 Screenshot sauvegardé : debug_real_login_url.png")
    
    # 8. Pause pour inspection manuelle
    print("\n⏸️  Pause de 10 secondes pour inspection...")
    time.sleep(10)
    
finally:
    driver.quit()
    print("\n✅ Navigateur fermé")
