import streamlit as st
import requests
import json
from datetime import datetime
import urllib.parse


@st.cache_data
def search_amazon_data(scannable_id, local_date, route_number):
    cookies = {
    'ubid-acbfr': '262-6341317-0090447',
    'lc-acbfr': 'fr_FR',
    'x-acbfr': '"BwKCSGEBXcVJHytwHNPcI?1XQrx6Oo7iU@52T0JHyaHyYV9MqIR7nXHCSgkjvr8@"',
    'at-acbfr': 'Atza|IwEBILm0mu0HQMDYQyjFcYE-MYuNehl2vFOCBH6fYWYBINlaTuFJ62gtnOpzYiDKsPNRMCJmk00R8Di9HjQAgUhc7PV79FZ9qKHkTYVQKfDGxYRrZH6QUIWlAK7Wwuc5vX2o6TXeDeHxAAtJwv0p7zKDR0t6TnFRlqc8dw2F80qFUSYfb3vHpCyJomsWXUDZjz2ARk4wSPx9XJgOjwxaU2vsU6KKqlDYDDKLcy-kotj6jiBI5A',
    'sess-at-acbfr': '"zdnrfxVbDWAXO7jAqNxsfqat1LMgNwwQQQ/qj270Tg8="',
    'x-amz-log-portal-locale': 'fr-FR',
    'cwr_u': '3fbea3d5-a1e9-4ac9-b370-b710f089551c',
    'ak_bmsc': 'AC1C03CED312BED2351E50514B20E657~000000000000000000000000000000~YAAQxNhLF+l8RqePAQAARJRFvhce4IQLRSi5xDgplQcig5zBtM/ebb4e0wVHj17Xb+w43NI4CSsMOf3OpoXbYv5XM9HV2L05KBlnZIkfJhIfQ9IEc3CMOrqlL5RrWBZ/4Mnmezl9/wIwuQVO0f/qLHYOF0NGVWSh7MbonUrcVXS+3lmU0cY6jJGMY2o6MCAiI18N7Gl3alTfD0KqKOL3kyW0F5mwkARTlMx6Iljhiu/cKA8AJhIRxObcfz7tSLFclw6QtCY/elLXP9/76w8hEpoiZ4gkiJ4ZNwrdqHZH7SNZnHGFTkZPo0FolQg7FNbSA7h9QT6eqvJtLeThJ2aUId1sWLL8kJGjK7odxceFFR8gxveKWS2U5/yUWRLhejrbAJZKUqsUSP1gqw==',
    'session-id': '260-0899321-4052131',
    'session-token': 'dFXc6jJ/ybcod+q2gowsAFrS2i8z1pLd15ACJRjICVu0Fjmjy9/LhGVxZxsvY6D8V2iQRu0BwkQs8J3vLViRzIBYSxMHtnswSxxBeTD+rv4uBwpajVLW8QAguP2uZrRZ9FBG7HWtfnQIxgWUpo2Ln8S2DWFznD1uedQEOv0yksqRh1PYUJh33feTq9eWG3heYSVj6n2zzZ4gNqbTUwao0V69rSRsYR2wyjP9DQ5Yk2YRIV5WuJKhke/UJMpvK3+R7Z5pSZ96w08vd1k5sXaSo9p62qxDXjjvuYF6DgqRVJ1qMF26s8bggviED0N/ORBamBQnGo3zTCVyVMSVeiWpGGnPxXO4ywHNgArsJB7Vcw+Z8AhOVVKylz7YwLhqGH3k',
    'session-id-time': '2082787201l',
    'bm_sv': 'B8CB14A577E6C71315EB5AB043D0D673~YAAQxNhLF3w9ZKePAQAAxACLvhclYeyErnL8GLve7UDiIztwjodk8qBw0wN5kwkN6phVoDmpmdFw1zQVGpg2gkQJoqekfmO5Logx1LQy5gzO7uIhEzt8lruZnq4Rugwe3zIFmcnFDvVM3Z5GtXuQcG0+IUO74/1EL4DDDWSro7lPSF1lk9MEn1F/RQLEdowopF9CaMTw7Gf3jaYK8F5U67egu8OWY2ulmgtlN43qs4X2U9fRwO7VFbWfj4BW+4N0~1',
    'cwr_s': 'eyJzZXNzaW9uSWQiOiJhOTBjYWQ5NC0zYzZlLTRlOGItYWIzOC1hOGEwNGI4ZTFhZDUiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjI2NTYsInBhZ2UiOnsicGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL2l0aW5lcmFyaWVzIiwicGFyZW50UGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL3JvdXRlcyIsImludGVyYWN0aW9uIjo5MCwicmVmZXJyZXIiOiJodHRwczovL2xvZ2lzdGljcy5hbWF6b24uZnIvb3BlcmF0aW9ucy9leGVjdXRpb24vaXRpbmVyYXJpZXM/b3BlcmF0aW9uVmlldz10cnVlJnByb3ZpZGVyPUFMTF9EUklWRVJTJnNlbGVjdGVkRGF5PTIwMjQtMDUtMjgmc2VydmljZUFyZWFJZD1kNDU5Nzg4Yi02YTczLTQ4ZjktYTcxMy04MWFmYTBjNTliNjYiLCJyZWZlcnJlckRvbWFpbiI6ImxvZ2lzdGljcy5hbWF6b24uZnIiLCJzdGFydCI6MTcxNjg4ODczMTI1Mn19',
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
                matching_infos.append({
                    'name': address_info['name'],
                    'address1': address_info['address1'],
                    'address2': address_info.get('address2', ''),
                    'postalCode': address_info['postalCode'],
                    'city': address_info['city'],
                    'phone': address_info.get('phone', '')
                })

    matching_infos = matching_infos[1:]
    return matching_infos
    
def share_on_whatsapp(result):
    message = f"Nom: {result['name']}\nAdresse 1: {result['address1']}\nAdresse 2: {result['address2']}\nCode postal: {result['postalCode']}\nVille: {result['city']}\nTéléphone: {result['phone']}"
    
    # Créez un lien WhatsApp avec le message pré-rempli
    whatsapp_link = f"https://wa.me/?text={urllib.parse.quote_plus(message)}"
    print("WhatsApp Link:", whatsapp_link)  # Ajoutez cette ligne
    
    # Affichez le lien généré
    st.success("Lien WhatsApp généré:")
    st.markdown(f"[Partager sur WhatsApp]({whatsapp_link})", unsafe_allow_html=True)
    
def main():
    # Définir l'icône de la page avec un emoji téléphone
    st.set_page_config(page_icon="📞", page_title="Amazon Client")

    st.title("Amazon Client")

    local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))
    route_number = st.text_input("Numéro de route :")
    scannable_id = st.text_input("Numéro de colis :")

    if st.button("Rechercher"):
        # Convertir scannable_id en majuscules
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
                
             # Ajoutez un bouton pour partager sur WhatsApp
            if st.button("Partager sur WhatsApp"):
                    share_on_whatsapp(result)

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
