import streamlit as st
import requests
import json
from datetime import datetime
import urllib.parse


@st.cache_data
def search_amazon_data(scannable_id, local_date, route_number):
    cookies = {
    'ubid-acbfr': '260-2431672-8131832',
    'lc-acbfr': 'fr_FR',
    'x-amz-log-portal-locale': 'fr-FR',
    'cwr_u': 'd39e1ae8-18c6-421b-8863-c299a6df6ff5',
    'i18n-prefs': 'EUR',
    's_vnum': '2170668689034%26vn%3D1',
    's_nr': '1738668693011-New',
    's_dslv': '1738668693011',
    'at-acbfr': 'Atza|IwEBIJSCbzd_cCIgPIr2gdNNy2of8TuBiHzTQTHA3ZU20HE12G-bmYxgyhZb2_4Zrfzq6FGMQG7iSfkBqFWff7HjT_jUSUKGAkZbvYbp20eI_nU2qfg_yTKx0IJhUYBXPr6peqm5nlfTb1WKNjRNnb4oZUC0Woj5urqo158EdvpxS0ZwVFA04xJWpoj0KoxF-IqNt2bvClxBcMVBP-E3FD6Y8cefI6xhP3obTmIucC_qNlegDQ',
    'sess-at-acbfr': '"e3repTrYwy0fUVIA0gZXqj8XvV9jYGW1Dkxm+TMXGqg="',
    'session-id-time': '2082787201l',
    'x-acbfr': 'tH2g?4IkNW71foI0esKgFNsWX9CL8YcDciWnA3@pnUh3fwvI?ORuClYJgbsLdl@z',
    'session-id': '258-8500938-2210138',
    'session-token': '82Lk6FReK8KevaJnlAWx/+5u66Kyu8o8PBRRwZjIIqhnMuopAzKK1Wj8GSgaU0MbDri5VBrKoqqJmfW8Yoc4tTuamGA1a3RzzXHeQRhIWRBdIqJK6GwrQcRZg4ydEDjmKGkBgGMuF8/KiNafwHVI3yPfYesWB2JGgsRD58KGrY4c9GmnuJ6JBHr0D75gkYRQryn9eJVh7E4O35xHsT/E3t6OuYIC06l77uXBL7ujNAGap8aOyBEXPNSAOGy/qc+zrUWhFMeSafvQUgHOPC2Z6xS9mOLFV3d5o9UNx39dpmOxOt3fk2rSB1qqm5Y+RFz0nb3dgFvuu4S+mWUxdV76StqHuTdY7wuMVkGOpkkqy86S1IPs4fCDx689sgmbxLZF',
    'cwr_s': 'eyJzZXNzaW9uSWQiOiJlODQ2YWMyOS03NDc1LTRhMGMtOWJmNC1kMGFlNGNjNGRjMGYiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjkxNSwicGFnZSI6eyJwYWdlSWQiOiIvb3BlcmF0aW9ucy9leGVjdXRpb24vcm91dGVzLzY3NTI1MzEtMjE5IiwicGFyZW50UGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL3JvdXRlcyIsImludGVyYWN0aW9uIjo0MCwicmVmZXJyZXIiOiIiLCJyZWZlcnJlckRvbWFpbiI6IiIsInN0YXJ0IjoxNzQ0NjI1OTc0NTc2fX0=',
}

    params = {
        'localDate': local_date,
        'serviceAreaId': 'd459788b-6a73-48f9-a713-81afa0c59b66',
    }

    response = requests.get('https://logistics.amazon.fr/operations/execution/api/summaries', params=params,
                            cookies=cookies)

    if response.status_code == 200:
        data = json.loads(response.text)
        all_route_ids = []

        for itinerary in data['itinerarySummaries']:
            route_ids = [route['routeId'] for route in itinerary['routes']]
            all_route_ids.extend(route_ids)

        prefixed_route_ids = [f"https://logistics.amazon.fr/operations/execution/api/routes/{route_id}" for route_id in
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

    local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2038, 1, 1))
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
