
import os
from dotenv import load_dotenv

class ModelLoader:
    def __init__(self):
        # Chargement des variables d’environnement (clé API)
        load_dotenv()
        self.api_key = os.getenv("llm_key")  # Assure-toi que ta clé est dans le fichier .env
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

        # Dictionnaire des modèles OpenRouter que tu veux utiliser
        self.models = {
            "deepseek_r1": "deepseek/deepseek-r1-0528-qwen3-8b:free",
            "qwen": "qwen/qwen1.5-7b-chat",
            "mistral": "mistralai/mistral-7b-instruct:free",
            "gpt-3.5": "openai/gpt-3.5-turbo",
            # Ajoute ici d'autres modèles si besoin
        }

    def get_model_name(self, key: str = "deepseek_r1"):
        """Retourne le nom complet du modèle compatible OpenRouter"""
        return self.models.get(key, self.models["deepseek_r1"])

    def get_headers(self):
        """Retourne les headers nécessaires pour appeler l’API OpenRouter"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_payload(self, messages, model_key="deepseek_r1", temperature=0.3):
        """Construit le payload à envoyer à l’API"""
        return {
            "model": self.get_model_name(model_key),
            "temperature": temperature,
            "messages": messages
        }

    def get_url(self):
        """Retourne l’URL de l’API OpenRouter"""
        return self.base_url
