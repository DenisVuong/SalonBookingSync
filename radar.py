import imaplib
import os
from dotenv import load_dotenv
import email

#on charge les variables du .env
load_dotenv()

user_email = os.getenv("YAHOO_EMAIL")
passwd = os.getenv("YAHOO_APP_PASSWORD")


#connection IMAP
mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
mail.login(user_email, passwd)

#Selectionne le mailbox

mail.select("inbox")

result, data = mail.search(None, "UNSEEN")
for num in data[0].split():
    result, msg_data = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    print(msg["subject"])

mail.logout()