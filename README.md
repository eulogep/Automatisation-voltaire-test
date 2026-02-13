# Projet Voltaire Automation Bot 🤖

Bot Selenium pour automatiser la connexion au Projet Voltaire et résoudre les exercices avec apprentissage automatique.

## 🚀 Installation

```bash
# Installer les dépendances
pip install -r requirements.txt
```

## ⚙️ Configuration initiale (IMPORTANT)

**Première utilisation** : Vous devez créer un profil Chrome dédié pour éviter les problèmes de cookies.

```bash
python setup_chrome_profile.py
```

Suivez les instructions à l'écran :

1. Chrome s'ouvrira automatiquement
2. Acceptez les cookies
3. Connectez-vous manuellement avec vos identifiants
4. Fermez Chrome

✅ **C'est tout !** Le bot réutilisera ce profil pour toutes les prochaines exécutions.

## 🧪 Tests

### Test de connexion complet

```bash
pytest test_projet_voltaire.py::test_projet_voltaire_full_flow --html=report.html --self-contained-html -v -s
```

### Scripts de débogage

```bash
# Trouver l'URL de connexion
python find_login_url.py

# Tester la soumission du formulaire
python debug_submit.py
```

## 🧠 VoltaireBrain - Système d'apprentissage

Le bot apprend de ses erreurs et stocke ses connaissances dans `voltaire_knowledge.json`.

**Fonctionnement** :

1. **Premier run** : Le bot se trompe et apprend des corrections
2. **Runs suivants** : Le bot devient de plus en plus intelligent
3. **Partage** : Échangez `voltaire_knowledge.json` entre étudiants pour un bot parfait !

## 📁 Structure du projet

```
projet_voltaire_tests/
├── conftest.py              # Configuration Pytest + WebDriver
├── test_projet_voltaire.py  # Test principal
├── voltaire_brain.py         # Système d'apprentissage
├── setup_chrome_profile.py   # Configuration profil Chrome
├── chrome_profile/           # Profil Chrome (généré)
├── screenshots/              # Screenshots de débogage
├── requirements.txt          # Dépendances Python
└── README.md                 # Ce fichier
```

## 🔧 Automatisation quotidienne

### Windows Task Scheduler

Créez une tâche planifiée pour exécuter le bot tous les jours :

```powershell
# Créer run_tests.bat
@echo off
cd /d "C:\Users\mabia\OneDrive\Desktop\Projet voltaire\projet_voltaire_tests"
.\venv\Scripts\python.exe -m pytest test_projet_voltaire.py::test_projet_voltaire_full_flow --html=report.html --self-contained-html
```

Puis configurez Task Scheduler :

1. Ouvrir "Planificateur de tâches"
2. Créer une tâche de base
3. Déclencheur : Tous les jours à 8h00
4. Action : Lancer `run_tests.bat`

## 📊 Credentials

Les identifiants sont stockés dans `test_projet_voltaire.py` :

- Email : `mabiala@et.esiea.fr`
- Mot de passe : `Jesusestseigneur2024*`

⚠️ **Sécurité** : Pour un usage en production, utilisez des variables d'environnement.

## 🐛 Débogage

### Problème de cookies

Si la bannière de cookies bloque encore :

```bash
# Recréer le profil Chrome
rm -rf chrome_profile
python setup_chrome_profile.py
```

### Screenshots

Tous les échecs génèrent des screenshots dans `screenshots/` avec timestamp.

## 📝 Git

```bash
# Commit après chaque modification importante
git add .
git commit -m "feat: Description de la modification"
```

## 📚 Documentation

- `walkthrough.md` : Documentation complète du projet
- `task.md` : Liste des tâches et progression
- `implementation_plan.md` : Plan d'implémentation détaillé

## 🎯 Prochaines étapes

- [ ] Finaliser la connexion avec profil Chrome
- [ ] Intégrer VoltaireBrain pour résoudre les exercices
- [ ] Créer `run_tests.bat` pour automatisation
- [ ] Configurer Windows Task Scheduler

---

**Créé par** : EULOGE MABIALA  
**Dernière mise à jour** : 2026-02-13
