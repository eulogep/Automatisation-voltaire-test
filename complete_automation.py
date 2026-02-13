import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from voltaire_brain import VoltaireBrain

# Configuration
EMAIL = "mabiala@et.esiea.fr"
PASSWORD = "Jesusestseigneur2024*"
KNOWLEDGE_FILE = "voltaire_knowledge.json"

class VoltaireAutomator:
    def __init__(self):
        self.brain = VoltaireBrain(KNOWLEDGE_FILE)
        self.setup_driver()
        self.wait = WebDriverWait(self.driver, 15)

    def setup_driver(self):
        options = Options()
        # En environnement sandbox Manus, on utilise le Chrome installé par défaut
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--start-maximized")
        
        # Désactiver les notifications et autres popups
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        
        # Masquer Selenium
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def human_type(self, element, text):
        """Simule une frappe humaine avec nettoyage préalable"""
        self.driver.execute_script("arguments[0].value = '';", element)
        time.sleep(0.3)
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

    def force_clear_cookies(self):
        """Supprime radicalement toute trace de bannière de cookies"""
        print("🧹 Nettoyage des overlays de cookies...")
        try:
            # Essayer de cliquer sur le bouton d'acceptation
            cookie_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
            print("✅ Bouton cookies cliqué")
            time.sleep(1)
        except:
            pass

        # Suppression agressive du DOM au cas où
        script = """
        ['onetrust-banner-sdk', 'onetrust-consent-sdk', 'ot-sdk-btn-floating'].forEach(id => {
            var el = document.getElementById(id);
            if (el) el.remove();
        });
        document.body.style.overflow = 'auto';
        document.body.style.pointerEvents = 'auto';
        document.documentElement.style.overflow = 'auto';
        """
        self.driver.execute_script(script)

    def login(self):
        print("📍 Connexion au Projet Voltaire...")
        self.driver.get("https://www.projet-voltaire.fr/")
        self.force_clear_cookies()

        try:
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Se connecter"))
            )
            login_btn.click()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Erreur bouton connexion: {e}. Tentative navigation directe.")
            self.driver.get("https://auth.projet-voltaire.fr/")

        self.force_clear_cookies()

        try:
            email_input = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Identifiant'], input[name='auth_login'], input[type='email']"))
            )
            self.human_type(email_input, EMAIL)

            pass_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Mot de passe'], input[name='auth_password'], input[type='password']")
            self.human_type(pass_input, PASSWORD)

            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.driver.execute_script("arguments[0].click();", submit_btn)
            
            # Attendre le dashboard
            self.wait.until(EC.url_contains("tableau-de-bord"))
            print("🎉 Connecté avec succès !")
        except Exception as e:
            print(f"❌ Échec de la connexion : {e}")
            self.driver.save_screenshot("login_error.png")
            raise

    def start_training(self):
        print("📚 Accès au module Orthographe...")
        try:
            self.driver.get("https://www.projet-voltaire.fr/mon-parcours/orthographe/")
            time.sleep(3)
            
            start_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entraînement')] | //a[contains(., 'Commencer')]"))
            )
            start_btn.click()
            print("🚀 Session d'entraînement démarrée !")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Impossible de lancer l'entraînement : {e}")
            # Fallback navigation directe si possible
            self.driver.get("https://compte.groupe-voltaire.fr/user/universe/1573/list")
            time.sleep(5)

    def get_full_sentence(self):
        """Extrait la phrase complète de l'exercice"""
        try:
            # Dans le Projet Voltaire, les mots sont souvent dans des spans avec des classes spécifiques
            # On essaie de reconstruire la phrase à partir des éléments textuels
            sentence_elements = self.driver.find_elements(By.CSS_SELECTOR, ".sentence span, .point-pointer")
            if not sentence_elements:
                # Fallback sur le conteneur principal de l'exercice
                exercise_container = self.driver.find_element(By.CSS_SELECTOR, ".exercise-content, #exercise")
                return exercise_container.text.strip()
            
            return " ".join([el.text for el in sentence_elements if el.text.strip()]).strip()
        except:
            return None

    def solve_exercise(self):
        """Logique de résolution d'un exercice unique gérant plusieurs types"""
        try:
            # Détecter le type d'exercice
            if self.driver.find_elements(By.CSS_SELECTOR, "input.input-field, .fill-blank"):
                return self.solve_fill_blank()
            elif self.driver.find_elements(By.CSS_SELECTOR, ".draggable, .dropzone"):
                return self.solve_drag_and_drop()
            else:
                return self.solve_standard_exercise()
        except Exception as e:
            print(f"⚠️ Erreur lors de la résolution : {e}")
            return False

    def solve_standard_exercise(self):
        """Exercice classique : cliquer sur la faute ou 'Pas de faute'"""
        sentence = self.get_full_sentence()
        if not sentence: return False
        print(f"📝 Phrase (Standard) : {sentence}")
        
        answer = self.brain.get_answer(sentence)
        if answer is not None:
            if answer == "Pas de faute":
                self.click_no_error()
            else:
                self.click_word(answer)
        else:
            # Apprentissage
            if random.random() > 0.2:
                self.click_no_error()
                self.learn_from_result(sentence, "Pas de faute")
            else:
                words = self.driver.find_elements(By.CLASS_NAME, "point-pointer")
                if words:
                    target = random.choice(words)
                    word_text = target.text
                    target.click()
                    self.learn_from_result(sentence, word_text)
        return True

    def solve_fill_blank(self):
        """Exercice de type texte à trous"""
        print("📝 Type détecté : Texte à trous")
        sentence = self.get_full_sentence()
        answer = self.brain.get_answer(f"FILL:{sentence}")
        
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input.input-field, .fill-blank")
        if answer and inputs:
            self.human_type(inputs[0], answer)
            inputs[0].send_keys(Keys.ENTER)
        else:
            # On ne peut pas deviner facilement, on attend ou on tente un mot commun
            print("🤔 Inconnu pour texte à trous.")
        return True

    def solve_drag_and_drop(self):
        """Exercice de type glisser-déposer"""
        print("📝 Type détecté : Glisser-déposer")
        # Logique simplifiée : on déplace le premier élément vers la première zone
        try:
            source = self.driver.find_element(By.CLASS_NAME, "draggable")
            target = self.driver.find_element(By.CLASS_NAME, "dropzone")
            from selenium.webdriver import ActionChains
            actions = ActionChains(self.driver)
            actions.drag_and_drop(source, target).perform()
            return True
        except:
            return False

    def click_no_error(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btn_no_error")))
            btn.click()
        except:
            # Fallback JS
            self.driver.execute_script("document.getElementById('btn_no_error').click();")

    def click_word(self, word_text):
        try:
            words = self.driver.find_elements(By.CLASS_NAME, "point-pointer")
            for w in words:
                if w.text.strip() == word_text.strip():
                    w.click()
                    return
            # Si non trouvé par texte exact, essayer de cliquer sur l'élément qui contient le texte
            self.driver.find_element(By.XPATH, f"//*[contains(@class, 'point-pointer') and contains(text(), '{word_text}')]").click()
        except:
            print(f"❌ Impossible de cliquer sur le mot : {word_text}")

    def learn_from_result(self, sentence, attempted_answer):
        """Analyse le feedback après un clic pour apprendre la bonne réponse"""
        time.sleep(2)
        try:
            # Vérifier si c'était correct
            # Souvent une classe 'correct' ou 'wrong' apparaît, ou un message de feedback
            feedback = self.driver.find_element(By.CSS_SELECTOR, ".feedback, .explanation").text
            
            if "Bravo" in feedback or "Correct" in feedback:
                self.brain.learn(sentence, attempted_answer if attempted_answer != "Pas de faute" else None)
            else:
                # Extraire la correction du texte d'explication
                # C'est ici que la logique devient complexe et dépend de la structure exacte
                # Pour l'instant, on marque comme inconnu pour réessayer plus tard ou on analyse l'explication
                print(f"❌ Erreur. Explication : {feedback[:100]}...")
                # Logique d'extraction de la correction à affiner selon les cas réels
        except:
            pass

    def run(self, iterations=10):
        try:
            self.login()
            self.start_training()
            
            for i in range(iterations):
                print(f"\n--- Exercice {i+1}/{iterations} ---")
                success = self.solve_exercise()
                if not success:
                    # Essayer de passer à l'exercice suivant si bloqué
                    try:
                        next_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Suivant')]")
                        next_btn.click()
                    except:
                        pass
                time.sleep(3)
                
            print("\n✅ Session terminée.")
            stats = self.brain.get_stats()
            print(f"📊 Stats cerveau : {stats}")
            
        finally:
            self.driver.quit()

if __name__ == "__main__":
    automator = VoltaireAutomator()
    automator.run(iterations=20)
