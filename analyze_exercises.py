"""
Script avec solution anti-crash : Override window.open + Simulation d'événements JS
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
import os

# Configuration
profile_dir = os.path.join(os.getcwd(), "chrome_profile")

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument(f"--user-data-dir={profile_dir}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

try:
    wait = WebDriverWait(driver, 15)

    print("=" * 70)
    print("SOLUTION ANTI-CRASH : Override window.open + Simulation JS")
    print("=" * 70)

    # 1. Connexion
    print("\n📍 Étape 1: Connexion...")
    driver.get("https://www.projet-voltaire.fr/")
    time.sleep(2)

    try:
        login_btn = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Se connecter"))
        )
        login_btn.click()
        time.sleep(2)

        email_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[placeholder='Identifiant'], input[type='email']",
                )
            )
        )
        if len(email_input.get_attribute("value") or "") > 5:
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            time.sleep(3)
            print("✅ Connecté")
    except Exception:
        print("ℹ️ Déjà connecté")

    # 2. Navigation vers universe/1573/list
    print("\n📍 Étape 2: Navigation vers Universe 1573...")
    driver.get("https://compte.groupe-voltaire.fr/user/universe/1573/list")
    time.sleep(4)
    print(f"✅ URL: {driver.current_url}")

    # 3. SOLUTION ANTI-CRASH
    print("\n📍 Étape 3: Application de la solution anti-crash...")

    # Override window.open pour forcer l'ouverture dans le même onglet
    driver.execute_script(
        "window.open = function(url) { window.location.href = url; };"
    )
    print("✅ window.open overridé (force same-tab)")

    # 4. Déclenchement contrôlé de l'entraînement
    print("\n📍 Étape 4: Déclenchement contrôlé de l'entraînement...")

    try:
        # Chercher le bouton ENTRAÎNEMENT
        btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'ENTRAÎNEMENT')]")
            )
        )
        print(f"✅ Bouton trouvé: {btn.text}")
        print(f"   Tag: {btn.tag_name}")
        print(f"   Class: {btn.get_attribute('class')}")
        print(f"   OnClick: {btn.get_attribute('onclick')}")

        # Scroll vers le bouton
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)

        # Simulation d'événements JS complets (mousedown -> mouseup -> click)
        print("\n🖱️ Simulation d'événements JS (mousedown → mouseup → click)...")
        driver.execute_script(
            """
            var evt = ['mousedown', 'mouseup', 'click'];
            var target = arguments[0];
            evt.forEach(function(type) {
                var e = document.createEvent('MouseEvents');
                e.initEvent(type, true, true);
                target.dispatchEvent(e);
            });
        """,
            btn,
        )

        print("🚀 Signal d'entraînement envoyé")
        print("⏳ Attente de la génération de session côté serveur (8 secondes)...")
        time.sleep(8)

        print(f"\n🔗 URL finale atteinte : {driver.current_url}")

        # Vérifier si on est sur la page d'apprentissage
        if (
            "apprentissage" in driver.current_url
            or "selection-module" in driver.current_url
        ):
            print("\n🎉 SUCCÈS : Page d'apprentissage atteinte !")
            print("=" * 70)

            # Screenshot
            driver.save_screenshot("screenshots/apprentissage_anti_crash_success.png")
            print("📸 Screenshot: apprentissage_anti_crash_success.png")

            # Analyser la page
            print("\n🔍 ANALYSE DE LA PAGE\n")

            # Texte de la page
            body_text = driver.find_element(By.TAG_NAME, "body").text
            print(f"Texte de la page (premiers 800 caractères):")
            print(body_text[:800])
            print("\n...")

            # Chercher les modules cibles
            print("\n\n🎯 RECHERCHE DES MODULES CIBLES\n")
            print("=" * 70)

            target_modules = [
                "Orthotypographie",
                "Les Fondamentaux Campus",
                "Fondamentaux Campus",
                "Fondamentaux",
            ]

            found_modules = []
            for module_name in target_modules:
                if module_name in body_text:
                    print(f"✅ '{module_name}' trouvé dans le texte")
                    found_modules.append(module_name)
                    try:
                        elem = driver.find_element(
                            By.XPATH, f"//*[contains(text(), '{module_name}')]"
                        )
                        print(
                            f"   Tag: {elem.tag_name}, Class: {elem.get_attribute('class')}"
                        )

                        # Chercher un élément cliquable associé
                        parent = elem.find_element(By.XPATH, "..")
                        clickables = parent.find_elements(
                            By.CSS_SELECTOR, "a, button, div[onclick]"
                        )
                        if clickables:
                            print(f"   Éléments cliquables: {len(clickables)}")
                            for clk in clickables[:2]:
                                print(f"      - {clk.tag_name}: '{clk.text[:50]}'")
                    except Exception as e:
                        print(f"   (Élément non localisable: {e})")
                else:
                    print(f"❌ '{module_name}' non trouvé")

            # Sauvegarder HTML
            with open("apprentissage_anti_crash.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("\n💾 HTML sauvegardé: apprentissage_anti_crash.html")

            # Si on a trouvé des modules, essayer d'en ouvrir un
            if found_modules:
                print("\n\n🚀 TENTATIVE D'ACCÈS À UN MODULE\n")
                print("=" * 70)

                module_to_try = found_modules[0]
                print(f"📍 Tentative d'accès à: {module_to_try}")

                try:
                    elem = driver.find_element(
                        By.XPATH, f"//*[contains(text(), '{module_to_try}')]"
                    )

                    # Chercher un lien/bouton cliquable
                    if elem.tag_name == "a":
                        elem.click()
                    else:
                        parent = elem.find_element(By.XPATH, "..")
                        clickable = parent.find_element(By.CSS_SELECTOR, "a, button")
                        clickable.click()

                    print("✅ Clic effectué")
                    time.sleep(5)

                    print(f"📍 URL du module: {driver.current_url}")
                    driver.save_screenshot(
                        f"screenshots/module_{module_to_try.replace(' ', '_')}.png"
                    )

                    # Analyser la structure de l'exercice
                    print("\n🔍 STRUCTURE DE L'EXERCICE\n")
                    print("=" * 70)

                    # Chercher les éléments d'exercice
                    exercise_text = driver.find_element(By.TAG_NAME, "body").text
                    print(f"Texte de l'exercice (premiers 500 caractères):")
                    print(exercise_text[:500])

                    # Sauvegarder HTML de l'exercice
                    with open("exercise_structure.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print("\n💾 HTML exercice sauvegardé: exercise_structure.html")

                except Exception as e:
                    print(f"⚠️ Erreur lors de l'accès au module: {e}")

        else:
            print("\n⚠️ Pas sur la page d'apprentissage")
            print(f"URL: {driver.current_url}")
            driver.save_screenshot("screenshots/not_apprentissage_anti_crash.png")

    except Exception as e:
        print(f"\n❌ Erreur lors du déclenchement: {e}")
        driver.save_screenshot("screenshots/error_anti_crash.png")

    print("\n⏸️ Pause de 30 secondes pour inspection...")
    time.sleep(30)

finally:
    driver.quit()
    print("\n✅ Terminé")
