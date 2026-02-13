"""
VoltaireBrain - Système d'apprentissage automatique pour Projet Voltaire

Ce module permet au bot d'apprendre de ses erreurs et de stocker ses connaissances
dans un fichier JSON persistant. Plus le bot s'entraîne, plus il devient intelligent.
"""

import json
import os


class VoltaireBrain:
    def __init__(self, filename="voltaire_knowledge.json"):
        self.filename = filename
        self.memory = self.load_memory()

    def load_memory(self):
        """Charge la mémoire depuis le fichier JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_memory(self):
        """Sauvegarde la mémoire dans le fichier JSON"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def get_answer(self, sentence):
        """
        Retourne le mot à cliquer si connu, sinon None

        Args:
            sentence (str): La phrase complète de l'exercice

        Returns:
            str or None: Le mot à cliquer, ou None si "Pas de faute"
        """
        return self.memory.get(sentence)

    def learn(self, sentence, correct_word):
        """
        Enregistre la règle apprise

        Args:
            sentence (str): La phrase complète de l'exercice
            correct_word (str or None): Le mot correct, ou None si "Pas de faute"
        """
        self.memory[sentence] = correct_word
        self.save_memory()
        if correct_word:
            print(f"📖 Nouveau savoir acquis : [{sentence}] -> {correct_word}")
        else:
            print(f"📖 Nouveau savoir acquis : [{sentence}] -> Pas de faute")

    def get_stats(self):
        """Retourne les statistiques d'apprentissage"""
        total = len(self.memory)
        no_error = sum(1 for v in self.memory.values() if v is None)
        with_error = total - no_error
        return {"total": total, "no_error": no_error, "with_error": with_error}
