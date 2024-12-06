import streamlit as st
import streamlit_authenticator as stauth
import json
from datetime import datetime, date
import requests
import urllib.parse


# Fichier pour stocker les données des demandes
REQUESTS_FILE = "requests.json"


# === Authentification ===
# Configuration des utilisateurs
users = {
    "user1": {"name": "Alice", "password": "password123"},
    "user2": {"name": "Bob", "password": "mypassword"},
}

# Hashage des mots de passe (une seule fois si non encore fait)
hashed_passwords = stauth.Hasher([users[user]["password"] for user in users]).generate()

authenticator = stauth.Authenticate(
    {user: {"name": users[user]["name"], "password": hashed_passwords[idx]} for idx, user in enumerate(users)},
    "auth_cookie",
    "auth_key",
    cookie_expiry_days=1,
)

# Interface de connexion
name, authentication_status, username = authenticator.login("Connexion", "main")

if authentication_status:
    st.success(f"Bienvenue, {name} !")
elif authentication_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect.")
elif authentication_status is None:
    st.warning("Veuillez vous connecter pour accéder à l'application.")
    st.stop()


# === Limitation des demandes ===
# Charger les données des demandes
def load_requests():
    try:
        with open(REQUESTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
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
if not can_request_today(username):
    st.error("Vous avez atteint votre limite quotidienne de 2 demandes.")
    st.stop()

# Afficher les demandes restantes
requests_data = load_requests()
today_requests = requests_data.get(username, {}).get(str(date.today()), 0)
st.info(f"Il vous reste {2 - today_requests} demande(s) aujourd'hui.")


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
