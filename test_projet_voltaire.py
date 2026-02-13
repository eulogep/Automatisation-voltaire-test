import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Configuration
EMAIL = "mabiala@et.esiea.fr"
PASSWORD = "Jesusestseigneur2024*"


def human_type(driver, element, text):
    """Simule une frappe humaine avec nettoyage préalable"""
    # Nettoyer le champ avec JavaScript (plus fiable que .clear())
    driver.execute_script("arguments[0].value = '';", element)
    time.sleep(0.3)

    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def force_clear_cookies(driver):
    """Supprime radicalement toute trace de bannière de cookies via injection CSS et JS"""
    print("🧹 Nettoyage agressif des overlays...")

    # ÉTAPE 1: Cliquer sur le bouton d'acceptation avec retry (important pour sauvegarder le choix)
    for attempt in range(3):
        try:
            cookie_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
            print(f"✅ Bouton cookies cliqué (tentative {attempt + 1})")
            time.sleep(1)

            # Vérifier que le bouton a disparu
            try:
                WebDriverWait(driver, 2).until(
                    EC.invisibility_of_element_located(
                        (By.ID, "onetrust-accept-btn-handler")
                    )
                )
                print("✅ Bannière disparue")
                break
            except Exception:
                print("⚠️ Bannière toujours présente, nouvelle tentative...")
                continue

        except Exception:
            if attempt == 0:
                print("ℹ️ Bouton cookies non trouvé")
            break

    # ÉTAPE 2: Suppression agressive du DOM
    script = """
    // 1. Supprimer les éléments par ID
    ['onetrust-banner-sdk', 'onetrust-consent-sdk', 'ot-sdk-btn-floating'].forEach(id => {
        var el = document.getElementById(id);
        if (el) el.remove();
    });
    
    // 2. Supprimer les voiles noirs (dark filters)
    var filters = document.getElementsByClassName('onetrust-pc-dark-filter');
    for (var i = 0; i < filters.length; i++) {
        filters[i].style.display = 'none';
        filters[i].remove();
    }

    // 3. Forcer la réactivation du scroll et des clics sur le BODY
    document.body.style.overflow = 'auto';
    document.body.style.pointerEvents = 'auto';
    document.documentElement.style.overflow = 'auto';
    """
    driver.execute_script(script)
    time.sleep(0.5)  # Laisser le DOM respirer


def test_projet_voltaire_full_flow(driver):
    wait = WebDriverWait(driver, 15)

    # 1. Homepage
    print("📍 Accès à la homepage...")
    driver.get("https://www.projet-voltaire.fr/")
    force_clear_cookies(driver)

    # 2. Cliquer sur "Se connecter"
    try:
        print("🔗 Recherche du bouton 'Se connecter'...")
        login_btn = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Se connecter"))
        )
        login_btn.click()
        print("✅ Clic sur 'Se connecter' effectué")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Erreur lors du clic : {e}")
        raise

    # 3. Gérer les cookies sur la page de connexion
    force_clear_cookies(driver)

    # 4. Remplir le formulaire avec les bons sélecteurs
    try:
        print(f"📍 URL actuelle: {driver.current_url}")
        print("🔍 Recherche du champ identifiant...")

        # Le champ utilise le placeholder "Identifiant" au lieu de name="auth_login"
        email_input = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "input[placeholder='Identifiant'], input[name='auth_login'], input[type='email']",
                )
            )
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", email_input)

        # Vérifier si le champ est déjà rempli (auto-fill Chrome)
        email_value = email_input.get_attribute("value") or ""

        if len(email_value) > 5:  # Si déjà rempli (au moins partiellement)
            print(f"✅ Email déjà pré-rempli par Chrome: {email_value[:10]}...")
        else:
            print("✍️ Saisie de l'email...")
            human_type(driver, email_input, EMAIL)

        # Mot de passe
        pass_input = driver.find_element(
            By.CSS_SELECTOR,
            "input[placeholder='Mot de passe'], input[name='auth_password'], input[type='password']",
        )

        pass_value = pass_input.get_attribute("value") or ""

        if len(pass_value) > 5:  # Si déjà rempli
            print(f"✅ Mot de passe déjà pré-rempli par Chrome")
        else:
            print("✍️ Saisie du mot de passe...")
            human_type(driver, pass_input, PASSWORD)

        # 5. Clic sur connexion
        print("🚀 Clic sur 'JE ME CONNECTE'...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        try:
            submit_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", submit_btn)

        print("✅ Tentative de connexion envoyée")

    except Exception as e:
        driver.save_screenshot("screenshots/fatal_error_login.png")
        print(f"❌ Erreur critique : {e}")
        raise

    # 6. Vérification de la redirection
    try:
        wait.until(EC.url_contains("tableau-de-bord"))
        print("🎉 Connecté avec succès au Dashboard !")
    except Exception:
        print(f"⚠️ Redirection lente ou URL inattendue : {driver.current_url}")
        driver.save_screenshot("screenshots/post_login.png")

    time.sleep(5)
    print(f"URL actuelle : {driver.current_url}")

    # On clique sur le module "Orthographe"
    try:
        # On cherche le bouton "Lancer", "Continuer" ou le titre "Orthographe"
        # Try finding by partial href as suggested
        orthographe_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, 'orthographe')]")
            )
        )
        orthographe_btn.click()
        print("📚 Module Orthographe ouvert")
    except:
        # Fallback : navigation directe au module
        driver.get("https://www.projet-voltaire.fr/mon-parcours/orthographe/")
        print("📍 Navigation directe vers Orthographe")

    # 5. Lancement de l'entraînement (Simulation de travail)
    try:
        start_btn = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Entraînement')] | //a[contains(., 'Commencer')]",
                )
            )
        )
        start_btn.click()
        print("🚀 Session d'entraînement démarrée !")

        # Simulation : On fait 3 exercices pour le test
        for i in range(3):
            time.sleep(3)
            # Logique simplifiée : soit on clique sur "Il n'y a pas de faute", soit sur un mot au hasard
            try:
                # Chercher le bouton "Il n'y a pas de faute"
                no_error_btn = driver.find_element(By.ID, "btn_no_error")
                no_error_btn.click()
            except:
                # Sinon on clique sur une zone de texte au hasard
                words = driver.find_elements(By.CLASS_NAME, "point-pointer")
                if words:
                    random.choice(words).click()

            print(f"📝 Exercice {i + 1} simulé")
            time.sleep(2)

    except Exception as e:
        print(f"ℹ️ Impossible de lancer l'exercice : {e}")

    # 6. Check final des statistiques
    driver.get("https://www.projet-voltaire.fr/mon-parcours/orthographe/statistiques")
    time.sleep(3)
    driver.save_screenshot("screenshots/final_progress.png")

    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "%" in body_text:
        print("📊 Statistiques récupérées avec succès")

    assert "403" not in body_text
