import imaplib
import os
from dotenv import load_dotenv
import email
from email.header import decode_header
from bs4 import BeautifulSoup

#on charge les variables du .env
load_dotenv()

user_email = os.getenv("YAHOO_EMAIL")
passwd = os.getenv("YAHOO_APP_PASSWORD")
email_adresses = ["noreply@planity.com", "noreply@pro.treatwell.com"]

#connection IMAP
mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
mail.login(user_email, passwd)

#Selectionne le mailbox
mail.select("inbox")

requete = f'UNSEEN OR FROM "{email_adresses[0]}" FROM "{email_adresses[1]}"'
result, data = mail.search(None, requete)

# On vérifie s'il y a des résultats
if data[0]:
    for num in data[0].split():
        result, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        # 1. Décoder le sujet (pour enlever les =?UTF-8... bizarres)
        sujet_brut = msg["subject"]
        sujet_decode, encoding = decode_header(sujet_brut)[0]
        if isinstance(sujet_decode, bytes):
            # S'il est en bytes, on le convertit en string
            sujet_decode = sujet_decode.decode(encoding if encoding else "utf-8")
            
        # 1.5. Détecter la source (Planity ou Treatwell)
        expediteur = msg.get("From", "")
        if "treatwell" in expediteur.lower():
            source = "Treatwell"
        elif "planity" in expediteur.lower():
            source = "Planity"
        else:
            source = "Inconnue"
            
        print(f"\n--- NOUVEL EMAIL ---")
        print(f"Source : {source}")
        print(f"Sujet : {sujet_decode}")
        
        # 2. Extraire le corps de l'email
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                # On cherche la partie HTML
                if content_type == "text/html":
                    html_content = part.get_payload(decode=True)
                    # On utilise BeautifulSoup pour nettoyer le HTML
                    soup = BeautifulSoup(html_content, "html.parser")
                    texte_propre = soup.get_text(separator="\n", strip=True)
                    print("Contenu :")
                    print(texte_propre)
                    break # On a trouvé le texte, on arrête de chercher dans les parties
        else:
            # Si le mail n'est pas multipart
            content_type = msg.get_content_type()
            if content_type == "text/html":
                html_content = msg.get_payload(decode=True)
                soup = BeautifulSoup(html_content, "html.parser")
                texte_propre = soup.get_text(separator="\n", strip=True)
                print("Contenu :")
                print(texte_propre)
            elif content_type == "text/plain":
                texte_propre = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                print("Contenu :")
                print(texte_propre)

mail.logout()