import streamlit as st
import hashlib
import json
from datetime import datetime, date
import requests
import urllib.parse
import os

# Fichier pour stocker les données des demandes
REQUESTS_FILE = "requests.json"

# === Authentification ===
# Fonction pour hacher les mots de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Configuration des utilisateurs (mots de passe hachés)
users = {
    "user1": {"name": "Alice", "password": hash_password("password123")},
    "user2": {"name": "Bob", "password": hash_password("mypassword")},
}

# Interface de connexion
def authenticate(username, password):
    if username in users and users[username]["password"] == hash_password(password):
        return True
    return False

# === Limitation des demandes ===
# Vérification de l'existence du fichier requests.json et création s'il n'existe pas
if not os.path.exists(REQUESTS_FILE):
    with open(REQUESTS_FILE, "w") as file:
        json.dump({}, file)

# Charger les données des demandes
def load_requests():
    try:
        with open(REQUESTS_FILE, "r") as file:
            data = file.read().strip()  # Lire le contenu du fichier
            if not data:  # Si le fichier est vide
                return {}
            return json.loads(data)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        st.error("Erreur de format du fichier de demandes.")
        return {}

# Enregistrer les données des demandes
def save_requests(data):
    with open(REQUESTS_FILE, "w") as file:
        json.dump(data, file)

# Vérifier et mettre à jour les demandes
def can_request_today(username):
    today = str(date.today())
    requests_data = load_requests()

    if username not in requests_data:
        requests_data[username] = {}

    user_requests = requests_data[username]
    if today not in user_requests:
        user_requests[today] = 0

    if user_requests[today] < 2:
        user_requests[today] += 1
        save_requests(requests_data)
        return True
    else:
        return False

# Limiter les demandes
def limit_requests(username):
    if not can_request_today(username):
        st.error("Vous avez atteint votre limite quotidienne de 2 demandes.")
        st.stop()

# === Fonction principale ===
def search_amazon_data(scannable_id, local_date, route_number):
    # Simulation d'une fonction récupérant des données d'Amazon
    return [
        {
            "name": "John Doe",
            "address1": "123 Main St",
            "address2": "Apt 4B",
            "postalCode": "75000",
            "city": "Paris",
            "phone": "0123456789",
        }
    ]

def share_on_whatsapp(result):
    message = f"Nom: {result['name']}\nAdresse 1: {result['address1']}\nAdresse 2: {result['address2']}\nCode postal: {result['postalCode']}\nVille: {result['city']}\nTéléphone: {result['phone']}"
    whatsapp_link = f"https://wa.me/?text={urllib.parse.quote_plus(message)}"
    return whatsapp_link

def main():
    st.title("Amazon Client")

    # Authentification de l'utilisateur
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if authenticate(username, password):
            st.success(f"Bienvenue, {users[username]['name']} !")
            
            # Limitation des demandes
            limit_requests(username)
            
            local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))
            route_number = st.text_input("Numéro de route :")
            scannable_id = st.text_input("Numéro de colis :")

            if st.button("Rechercher"):
                scannable_id = scannable_id.upper()
                formatted_date = local_date.strftime("%Y-%m-%d")
                results = search_amazon_data(scannable_id, formatted_date, route_number)

                if not results:
                    st.warning("Aucun résultat trouvé.")
                else:
                    for result in results:
                        st.write("Nom :", result['name'])
                        st.write("Adresse 1 :", result['address1'])
                        st.write("Adresse 2 :", result['address2'])
                        st.write("Code postal :", result['postalCode'])
                        st.write("Ville :", result['city'])
                        st.write("Téléphone :", result['phone'])
                        st.write("-" * 30)

                    whatsapp_link = share_on_whatsapp(results[0])
                    st.markdown(f'<a href="{whatsapp_link}" target="_blank">Partager sur WhatsApp</a>', unsafe_allow_html=True)

        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

    # Ajout du pied de page
    st.markdown(
        """
        <div style="text-align:center; margin-top: 30px; color: #888;">
            <hr>
            <p>© 2024 Big BoSs. Tous droits réservés.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
