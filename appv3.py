import streamlit as st
import requests
import json
from datetime import datetime
import urllib.parse


@st.cache_data
def search_amazon_data(local_date):
    cookies = {
        'lc-acbfr': 'fr_FR',
        # Ajoutez vos cookies ici
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

        # Préfixer les URLs pour chaque route
        prefixed_route_ids = [
            f"https://logistics.amazon.fr/operations/execution/api/routes/{route_id}" for route_id in all_route_ids
        ]

        # Récupérer les données de chaque route
        all_route_data = []
        for route_link in prefixed_route_ids:
            route_response = requests.get(route_link, cookies=cookies)
            if route_response.status_code == 200:
                route_data = json.loads(route_response.text)
                all_route_data.append(route_data)
            else:
                st.error(f"Échec pour l'URL {route_link} (Code : {route_response.status_code})")

        return all_route_data
    else:
        st.error("Échec de la récupération des données logistiques Amazon.")
        return None


def extract_all_scannable_ids(route_data_list):
    all_scannable_infos = []

    for route_data in route_data_list:
        for stop in route_data['routePlan']['stopList']:
            for package in stop['stopDetails']['packageList']:
                address_info = stop['stopDetails']['address']
                all_scannable_infos.append({
                    'scannableId': package['scannableId'],
                    'name': address_info['name'],
                    'address1': address_info['address1'],
                    'address2': address_info.get('address2', ''),
                    'postalCode': address_info['postalCode'],
                    'city': address_info['city'],
                    'phone': address_info.get('phone', '')
                })

    return all_scannable_infos


def share_on_whatsapp(result):
    message = f"Nom: {result['name']}\nAdresse 1: {result['address1']}\nAdresse 2: {result['address2']}\nCode postal: {result['postalCode']}\nVille: {result['city']}\nTéléphone: {result['phone']}"
    whatsapp_link = f"https://wa.me/?text={urllib.parse.quote_plus(message)}"
    return whatsapp_link


def main():
    # Définir l'icône de la page avec un emoji téléphone
    st.set_page_config(page_icon="📞", page_title="Amazon Client")

    st.title("Amazon Client - Récupération de tous les Scannable IDs")

    local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))

    if st.button("Rechercher toutes les données"):
        formatted_date = local_date.strftime("%Y-%m-%d")
        route_data_list = search_amazon_data(formatted_date)

        if route_data_list:
            scannable_infos = extract_all_scannable_ids(route_data_list)

            if not scannable_infos:
                st.warning("Aucun scannable ID trouvé.")
            else:
                for info in scannable_infos:
                    st.write("Scannable ID :", info['scannableId'])
                    st.write("Nom :", info['name'])
                    st.write("Adresse 1 :", info['address1'])
                    st.write("Adresse 2 :", info['address2'])
                    st.write("Code postal :", info['postalCode'])
                    st.write("Ville :", info['city'])
                    st.write("Téléphone :", info['phone'])
                    st.write("-" * 30)

                    # Lien WhatsApp pour partager les informations
                    whatsapp_link = share_on_whatsapp(info)
                    st.markdown(
                        f'<a href="{whatsapp_link}" target="_blank">Partager {info["scannableId"]} sur WhatsApp</a>',
                        unsafe_allow_html=True
                    )

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
