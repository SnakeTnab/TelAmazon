import streamlit as st
import requests
import json
from datetime import datetime
import urllib.parse


@st.cache_data
def search_amazon_data(scannable_id, local_date, route_number):
    cookies = {
        'ubid-acbfr': '257-2265996-3861609',
        '_fbp': 'fb.1.1688889150202.664494500',
        'adobeujs-optin': '%7B%22aam%22%3Atrue%2C%22adcloud%22%3Atrue%2C%22aa%22%3Atrue%2C%22campaign%22%3Afalse%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Afalse%2C%22target%22%3Atrue%2C%22mediaaa%22%3Afalse%7D',
        'AMCV_5E35755F5B7C1B910A495C46%40AdobeOrg': '1176715910%7CMCIDTS%7C19578%7CMCMID%7C09685279412664892150992027312307073326%7CMCAAMLH-1692118645%7C6%7CMCAAMB-1692118645%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1691521045s%7CNONE%7CvVersion%7C5.4.0%7CMCCIDH%7C-540876677',
        'mbox': 'PC#40f6ebc7592e48f587b3695926462642.37_0#1754758646|session#d50fa556a4574f88930e0582aa7d1249#1691515706',
        'adcloud': '{%22_les_lsc%22:%221691513845831%2Camazon.fr%2C1699379845%22%2C%22_les_v%22:%22y%2Camazon.fr%2C1691515645%22}',
        'i18n-prefs': 'EUR',
        'x-amz-log-portal-locale': 'fr-FR',
        'sst-acbfr': 'Sst1|PQHk2jLw7YN8whewhd0X0q5nB2EPXQDh_RfZwQF-brr4UjjLfFivbM7aQREETg3q2qb1EJWExtUDGeC1EvZ4jOT71LJhJXsB07RkCPGTfV_cu7K5_fG56gcFaJo0carqGDI8_AY5Ym6LPDxt8FqiTvvyb3SDwkRBygaWY5VvrJbmXVtU74awmVbNouSwZrBYJNxjYRxcg5mh9upS0lD5MgHZmKDdU0-euxu_dzGChXOWYb__QrBzrhlFU_UYkV6xqv7A',
        'lc-acbfr': 'fr_FR',
        'cwr_u': '11afc0a5-bae3-426e-b018-fb8440d1d226',
        'x-acbfr': '"sxwLBfc93YhSSCATYmpYlSw0NKObrNCrm7f@cdVH?GV?IsHRh8NfwnHz7LrMPPgQ"',
        'at-acbfr': 'Atza|IwEBIDdZqBtsU_Hubxv_DtMzDEuPcSHNvZbXRGjJF2e37-LeQ6tA-6VkscNQaerEWerQnkoNkLdQ9lA2bwSGqG6cD0q2_hwJBp-s5P3QGofcgyNiL8xGw5utjIZUgUrHMmCPuwJPN3_cbBKbj-2CwUHWG3ySOHweVvSlW8wXZb5_9M1SNKaE0fhD9RvKhtWcYIBXBJODPnxgFVS3_JJ2RbTtnHXMgf6aVGDuS3A9j0MVKBXzSw',
        'sess-at-acbfr': '"RF+P1GVQfYv8RVHsPJimb9xqpwAkGsJmEm8+iHTGzX0="',
        'session-id-time': '2082787201l',
        'session-id': '258-5386277-8061415',
        'session-token': 'rK9Q3J0KJXBh+n1HeR8pyvUQPH8vGD/ICDIsHoLWe3AckYndix0JM9zzQcoSISfCwDp3a4cmi4ZDcUTGENDNRSjIO1JewZmt2picD5QEsPNOQT8wqoac+QMsQ5hAQAdlxqau+WkuWUJJZYDW8j88MKQmnQ97MUoaemr58A3TUxm/wTyay1iP4eEGzvwLTL4UvGDt3YiJbt6IJNCy5jVp9rbm4bxuuY8C21BIVtbQNXDTUt1TboyLLGzmM7AnkXOX1sOrft/s1S0YLyyPqRNR0EdUrDMxOPwdwrDBHfBfEXW8o8wtaSod0ykgK7T9xVNo1ijG86+/ILBgMZ0H/2qhKEHL9GXJnXo4h7PNpF245Jn15Ih7aBK2lm9mKiV6tJ5A',
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
