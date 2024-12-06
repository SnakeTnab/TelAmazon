import streamlit as st
import hashlib
import json
from datetime import datetime, date
import requests
import urllib.parse
import os
import bcrypt
import logging

# Fichier pour stocker les données des demandes
REQUESTS_FILE = "requests.json"

# === Authentification ===
# Fonction pour hacher les mots de passe avec bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Fonction pour vérifier le mot de passe
def authenticate(username, password):
    if username in users and bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        return True
    return False

# Configuration des utilisateurs (mots de passe hachés)
users = {
    "user1": {"name": "Alice", "password": hash_password("password123")},
    "user2": {"name": "Bob", "password": hash_password("mypassword")},
}

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
    try:
        with open(REQUESTS_FILE, "w") as file:
            json.dump(data, file)
    except Exception as e:
        logging.error(f"Erreur lors de l'enregistrement des demandes: {e}")
        st.error("Impossible d'enregistrer vos demandes.")

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
    cookies = {
        'lc-acbfr': 'fr_FR',
        'x-amz-log-portal-locale': 'fr-FR',
        'cwr_u': '3fbea3d5-a1e9-4ac9-b370-b710f089551c',
        'i18n-prefs': 'EUR',
        'ubid-acbfr': '261-3161003-9190349',
        'x-acbfr': '"wb3elbf21ilNOQyPpgz9Z@6pVE59waPCFCc0REM4K?D3ERJIgnZnnRiYxupAMuD@"',
        'at-acbfr': 'Atza|IwEBIE5RavpwW_0iHxx5RS6KyZUXUbx4VHV0_LOi71z5zaj_NbvyiYlC_vcdhgYPYOWOeVRaMqcq5HCjBBf62hKZul4wYsFFkck2pVtJD6ccmtn7tMidsLqsJHpZM2ajmEbNQ-eR1OR8t2GvwAqzEjyjMyAj4Uu6YsZrSAh5jE9HxXqma5fqPeWLbwwRAwsGJU_QeuSdd_SrARqeKlPszhzM4UQLRFtn2PcWVh9Y3AkZDYqv6Q',
        'sess-at-acbfr': '"JUALMi0mz21adDYwUdXsuOC7qMbxyBMROAhB6KJtAHI="',
        'session-id-time': '2082787201l',
        'ak_bmsc': 'D794ED3D9DCA2C6BDD1494301730E770~000000000000000000000000000000~YAAQz9hLF0aeqf+QAQAA7Ba0Jxhgd3LyPJkhxeSK3gnTS9VdvSHSB61owUTrlwYyb5Z+V+w50iY7rAhqKASxYoeUlry1opcuOU70XKwRAQ5UaGaIwNThQILwOqBvOTGvLUzRxXmzuO8f6oB8kiuh1kyY46eMmTMkCoHj0Jnvyh4jA62pHCRvHUc9o0YJjBNEuT2sP1kVkhU7FwlXzMjdKJwrZ6UXvO95obTJHi9b2KDHbTzz+STQu2fvExpv09wzQyqd30Lo3O8CEyzqcGAYxnB1TdriXMRbM2h2m49C508TS/Uijm9iVt1EgoUYi0E5XRaCA9t1pGQ2rTdXJ1V7llOTi3xKGd8Dx9iQow43Hn8rwN1bpYVO/MgGBPdBSI+32/rnO+kLd1qwrg==',
        'session-id': '258-3085241-4888146',
        'session-token': 'XCshqmMy2tEksfNzi0AOmv+If8ug67KKfsLdr4vu1bE5PPX8TR8meQujgZ5efPEEMegesYZsQFr8DXOITAd2shjCa/gSNVDE5/ZqwaTlfGXhmvtbr0Txfh36FzmMIedK42wAOXdZ/NwgMgbjVvdLZjU73diLYTOnXGeMkgzKetQl1Pc501bwxsUZIuUeIG5pIgyEbM9C4+xIc9vhyJYYq/3cdfLUtq3F4cHjPX3pLtuvtOCWoF5eY8ItHdTAGEYFMO6JzyXDuCCnBJ3vGrV8ajw5ZbBno48WiyqTl5gpvE6uOWkyro5YlKFxUrYsPYAhoxhCUloxqJ4B5fau7j7bKc/waYRcK3ehdvErBZcS0VQ',
    }

    params = {
        'localDate': local_date,
        'serviceAreaId': 'd459788b-6a73-48f9-a713-81afa0c59b66',
    }

    response = requests.get('https://logistics.amazon.fr/operations/execution/api/summaries', params=params, cookies=cookies)

    if response.status_code == 200:
        data = json.loads(response.text)
        all_route_ids = []

        for itinerary in data['itinerarySummaries']:
            route_ids = [route['routeId'] for route in itinerary['routes']]
            all_route_ids.extend(route_ids)

        prefixed_route_ids = [f"https://logistics.amazon.fr/operations/execution/api/routes/{route_id}" for route_id in all_route_ids]

        if route_number.isdigit():
            route_number = int(route_number)
            matching_route_links = []

            for route_link in prefixed_route_ids:
                parts = route_link.split('/')
                last_part = parts[-1]
                route_id = last_part.split('-')[-1]

                if route_id.isdigit() and int(route_id) == route_number:
                    matching_route_links.append(route_link)

            if matching_route_links:
                for route_link in matching_route_links:
                    route_response = requests.get(route_link, cookies=cookies)

                    if route_response.status_code == 200:
                        route_data = json.loads(route_response.text)
                    else:
                        st.error(f"Échec de la récupération des données pour l'URL {route_link} avec le code d'état : {route_response.status_code}")
            else:
                st.warning(f"Aucune URL correspondante trouvée pour le numéro de route {route_number}.")
        else:
            st.warning("Le numéro de route doit être un entier.")
    else:
        st.error("Échec de la récupération des données logistiques Amazon.")

    infos = get_info_by_scannable_id(route_data, scannable_id)
    return infos

def get_info_by_scannable_id(route_data, scannable_id):
    matching_infos = []

    for stop in route_data['routePlan']['stopList']:
        for package in stop['stopDetails']['packageList']:
            if package['scannableId'] == scannable_id:
                address_info = stop['stopDetails']['address']
                stop_time_info = stop['stopDetails']['stopTime']
                matching_infos.append(f"Address: {address_info}, Stop Time: {stop_time_info}")
    return matching_infos

# === Interface Utilisateur ===
st.title("Application de Recherche Logistique Amazon")

# Authentification
if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.username == "":
    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(username_input, password_input):
            st.session_state.username = username_input
            st.success(f"Bienvenue {username_input}!")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    st.write(f"Bonjour, {st.session_state.username}!")
    limit_requests(st.session_state.username)

    # Collecte des données pour la recherche
    scannable_id = st.text_input("Scannable ID")
    local_date = st.date_input("Date")
    route_number = st.text_input("Numéro de route")

    if st.button("Rechercher"):
        infos = search_amazon_data(scannable_id, local_date, route_number)
        st.write(infos)
        st.button("Se déconnecter", on_click=lambda: st.session_state.clear())
