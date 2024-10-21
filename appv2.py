import streamlit as st
import requests
import json
from datetime import datetime
import urllib.parse


@st.cache_data
def search_amazon_data(scannable_id, local_date, route_number):
    cookies = {
    'session-id': '257-9305368-7376529',
    'session-id-time': '2082787201l',
    'ubid-acbuk': '259-3886438-1172934',
    'session-token': 'TOYGxkagi/LbezUEOr4ik4ACtGgPCM/yC0eZHX5NS6hmJN3XVzxnWweCPaK5Z0qLS2lTEqd3ykC7P9AJF7ECeijkg7rjnWUz1WtGJT0iG3smjwnMo7bdzDVoWyqoDRCR8Y92fs++8X08VQ/Cvq8BAsts7ECsmlBe4yOaCoKLASmrZ8Wv6i/xYrX905PhxFEay4PugLw0CHRHCrWEUu9UYO+HBaKfjxugfkzVISlHuUGS19eWmljLBDfJcSihCDZ6OofKRHLHJrVmr0RzB0LdAZ4OvWEVY6lvqiX7EBVZeBzfwR/CoKnnrvfLHZL1ZUcVc944kYdFHYidI0up5ml87I8G21b/IxloabczcchuazE',
    'x-amz-log-portal-locale': 'en-GB',
    'cwr_u': 'b902c16b-a658-432d-be56-c64529dc87c3',
    'lc-acbuk': 'en_GB',
    'csm-hit': 'tb:s-76XZ6J2BRK7K5C9MCHZY^|1705600193184&t:1705600194211&adb:adblk_no',
    'i18n-prefs': 'GBP',
    'av-timezone': 'Europe/Paris',
    'JSESSIONID': 'DD9D6A753E8A68E56BB4947B18152538',
    'cwr_s': 'eyJzZXNzaW9uSWQiOiJiNjk0YmQ4MC1lMWQ1LTRkMTUtYTdjNy1mNDUxOWZhODkxNjkiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjgxNCwicGFnZSI6eyJwYWdlSWQiOiIvaW50ZXJuYWwvb3BlcmF0aW9ucy9leGVjdXRpb24vZHYvcm91dGVzLzY0MDU4MDYtMTE5IiwicGFyZW50UGFnZUlkIjoiL2ludGVybmFsL29wZXJhdGlvbnMvZXhlY3V0aW9uL2R2L3JvdXRlcyIsImludGVyYWN0aW9uIjoyOCwicmVmZXJyZXIiOiJodHRwczovL2xvZ2lzdGljcy5hbWF6b24uY28udWsvcGVyZm9ybWFuY2U/cGFnZUlkPWRzcF9kYXNoYm9hcmRfb3ZlcnZpZXcmc3RhdGlvbj1EWEUxJmNvbXBhbnlJZD1lNmRlYWY3OS1iODViLTQ0MjEtOTMwMS1kYThiYTliMzVkY2ImdGFiSWQ9b3ZlcnZpZXctZHNwLXdlZWtseS10YWImdGltZUZyYW1lPVdlZWtseSZ0bz0yMDI0LVc0MiIsInJlZmVycmVyRG9tYWluIjoibG9naXN0aWNzLmFtYXpvbi5jby51ayIsInN0YXJ0IjoxNzI5NTI0NDc4MDA5fX0=',
    'amzn_sso_rfp': 'ecee0cc1f91dfde1',
    'logistics-federate-token': 'eyJraWQiOiJiNzU3Y2QwNmY0N2YzMmIzOTQ1MjBmM2Q0MDljZTQyZCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJhdWQiOiJMb2dpc3RpY3NQb3J0YWwtRVUtUHJvZC1GZWRlcmF0ZVByb2ZpbGUiLCJzdWIiOiJqdGlnaGlsZSIsIm5iZiI6MTcyOTUxNjk1NywiYXV0aF90aW1lIjoxNzI5NTE2NjQ1LCJpc3MiOiJodHRwczovL2lkcC5mZWRlcmF0ZS5hbWF6b24uY29tIiwiZXhwIjoxNzI5NTMxMzU3LCJmZWRlcmF0ZV90b2tlbl9wdXJwb3NlIjoiaWRfdG9rZW4iLCJpYXQiOjE3Mjk1MTY5NTcsIm5vbmNlIjoibm9uY2UiLCJqdGkiOiJJRC4xZjU5YmRkZC04MDM2LTQ2MDYtYmYwNC1lMTczMzg3YzZhNjAifQ.mQlZD7VgcqbYL5RWhW696K4GDso-3wEFqhKqqMg56sbwwlQ2jYp2Vj86UROys3a9BQbVBBfBkB6aSbhwOzpOIa4csg6FAingOogjrr0gN7CV4hg9H8I2IhLDw4P-g2kO8ZceE8Y493NjZHVDZ2pjOaolFGZTEwMagkbvlbLn86l3aObLmvRwzSXJzlMHEdOKiuCe5s-8ZrFr16CQQ0VxevzOyUqziI_oYR4XOBrlHEgVRHQOHUeVZB4CPYF8ByExvugcvdhx_apN3saNSAe3OQ7ZBKMLa2mIMkZBz2n_5P3fYSBcPMR3v9TRsU6au9VcgBNPi_czcI11HGnhiPhkpg',
    'logistics-federate-user-id': 'jtighile',
}

    params = {
        'localDate': local_date,
        'serviceAreaId': 'd459788b-6a73-48f9-a713-81afa0c59b66',
    }

    response = requests.get('https://logistics.amazon.co.uk/internal/operations/execution/api/route-summaries', params=params,
                            cookies=cookies)

    if response.status_code == 200:
        data = json.loads(response.text)
        all_route_ids = []

        for itinerary in data['rmsRouteSummaries']:
            route_ids = [route['routeId'] for route in itinerary['routes']]
            all_route_ids.extend(route_ids)

        prefixed_route_ids = [f"https://logistics.amazon.co.uk/internal/operations/execution/api/route-details/{route_id}" for route_id in
                              all_route_ids]

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
                        st.error(
                            f"Échec de la récupération des données pour l'URL {route_link} avec le code d'état : {route_response.status_code}")
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
    return whatsapp_link


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
            whatsapp_link = share_on_whatsapp(result)
            st.markdown(f'<a href="{whatsapp_link}" target="_blank">Partager sur WhatsApp</a>', unsafe_allow_html=True)

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
