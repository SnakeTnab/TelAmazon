import streamlit as st
import requests
import json
from datetime import datetime

@st.cache_data
def search_amazon_data_by_route(local_date, route_number):
    cookies = {
        'lc-acbfr': 'fr_FR',
        'x-amz-log-portal-locale': 'fr-FR',
        # Ajoutez d'autres cookies si nécessaire
    }

    params = {
        'localDate': local_date,
        'serviceAreaId': 'd459788b-6a73-48f9-a713-81afa0c59b66',
    }

    response = requests.get('https://logistics.amazon.fr/operations/execution/api/summaries', params=params, cookies=cookies)

    if response.status_code == 200:
        data = json.loads(response.text)
        all_route_ids = []

        st.write("Itinéraires trouvés :", data['itinerarySummaries'])

        for itinerary in data['itinerarySummaries']:
            route_ids = [route['routeId'] for route in itinerary['routes']]
            all_route_ids.extend(route_ids)

        # Rechercher le numéro de route correspondant
        if route_number.isdigit():
            route_number = int(route_number)
            for route_id in all_route_ids:
                # Extraire le numéro de route à partir de route_id
                parts = route_id.split('-')
                if len(parts) > 1 and parts[-1].isdigit():  # Vérifie si le dernier élément est un numéro
                    extracted_route_number = int(parts[-1])
                    if extracted_route_number == route_number:
                        route_link = f"https://logistics.amazon.fr/operations/execution/api/routes/{route_id}"
                        
                        # Afficher les liens générés
                        st.write("Lien de route testé :", route_link)

                        route_response = requests.get(route_link, cookies=cookies)

                        if route_response.status_code == 200:
                            try:
                                route_data = json.loads(route_response.text)
                                if "routePlan" in route_data:
                                    return extract_simple_info(route_data)
                                else:
                                    st.error("Structure inattendue dans les données de la route.")
                            except json.JSONDecodeError:
                                st.error("Erreur lors de la conversion JSON pour la route :", route_link)
                        else:
                            st.error(
                                f"Échec de la récupération des données pour l'URL {route_link} avec le code d'état : {route_response.status_code}")
        else:
            st.warning("Le numéro de route doit être un entier.")
    else:
        st.error("Échec de la récupération des données logistiques Amazon.")

    return []

def extract_simple_info(route_data):
    all_infos = []
    for stop in route_data.get('routePlan', {}).get('stopList', []):
        address_info = stop['stopDetails']['address']
        all_infos.append({
            'name': address_info['name'],
            'address1': address_info['address1'],
            'address2': address_info.get('address2', ''),
            'postalCode': address_info['postalCode'],
            'city': address_info['city'],
            'phone': address_info.get('phone', '')
        })
    return all_infos


def main():
    # Définir l'icône de la page avec un emoji téléphone
    st.set_page_config(page_icon="📞", page_title="Amazon Client")

    st.title("Amazon Client")

    local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))
    route_number = st.text_input("Numéro de route :")

    if st.button("Rechercher"):
        formatted_date = local_date.strftime("%Y-%m-%d")
        results = search_amazon_data_by_route(formatted_date, route_number)

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
