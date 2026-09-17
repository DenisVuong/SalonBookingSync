import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")



def extraire_donnees(texte_email, source):
    client = genai.Client(api_key=api_key)
    prompt = "Tu es un assistant qui extrait les détails d'une réservation de salon de manucure, je vais te donner un mails provenant de {source}. Renvoie UNIQUEMENT un objet JSON valide avec les clés : prestation, employe, heure_debut, heure_fin, telephone, nom, prenom. Ne rajoute pas de texte avant ou après."

    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = prompt,
    )

    return response.json.loads()
