"""
Script pour créer un profil Chrome dédié au bot Projet Voltaire
Exécutez ce script, puis connectez-vous manuellement UNE FOIS.
Chrome mémorisera les cookies et le bot pourra les réutiliser.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chemin du profil Chrome dédié
PROFILE_DIR = os.path.join(os.getcwd(), "chrome_profile")

print("=" * 60)
print("CONFIGURATION DU PROFIL CHROME POUR PROJET VOLTAIRE")
print("=" * 60)
print()
print(f"📁 Profil Chrome sera créé dans : {PROFILE_DIR}")
print()
print("📋 INSTRUCTIONS :")
print("1. Chrome va s'ouvrir automatiquement")
print("2. Acceptez les cookies en cliquant sur 'Accepter et fermer'")
print("3. Cliquez sur 'Se connecter'")
print("4. Entrez vos identifiants :")
print("   - Email : mabiala@et.esiea.fr")
print("   - Mot de passe : Jesusestseigneur2024*")
print("5. Validez la connexion")
print("6. Attendez d'être sur le dashboard")
print("7. Fermez Chrome manuellement")
print()
print("⚠️  IMPORTANT : Ne fermez PAS cette fenêtre avant d'avoir fermé Chrome !")
print()
input("Appuyez sur ENTRÉE pour lancer Chrome...")

# Configuration Chrome avec profil persistant
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")

print("\n🚀 Lancement de Chrome...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # Ouvrir la page d'accueil
    driver.get("https://www.projet-voltaire.fr/")
    
    print("\n✅ Chrome ouvert !")
    print("\n📝 Suivez les instructions ci-dessus pour vous connecter manuellement.")
    print("   Une fois connecté, vous pouvez fermer Chrome.")
    print("\n⏳ En attente de fermeture de Chrome...")
    
    # Attendre que l'utilisateur ferme Chrome
    while True:
        try:
            driver.current_url
            time.sleep(2)
        except Exception:
            break
    
    print("\n✅ Chrome fermé !")
    print(f"\n🎉 Profil Chrome configuré avec succès dans : {PROFILE_DIR}")
    print("\n📌 Le bot utilisera maintenant ce profil pour éviter les cookies.")
    print("   Vous n'aurez plus besoin de vous connecter manuellement !")
    
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    driver.quit()
