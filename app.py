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
    'x-amz-log-portal-locale': 'fr-FR',
    'cwr_u': '3fbea3d5-a1e9-4ac9-b370-b710f089551c',
    'i18n-prefs': 'EUR',
    'ak_bmsc': '4AF8774629765782B190AC0571B0C322~000000000000000000000000000000~YAAQxNhLF4lkqbiQAQAAHluRuxiIoArE9WZsmU0Kz1zpxMUlXj7rh4CcQ2o/dNNE0i+CcV79RXwGE4pGpGhYNZDCHdrxPs0aSv6OMpqJeE65/Ni5U1V6j52GI60F5wk/0cdzN1Pnvt7Ns8oA8C+lk67+q+6XfFd6saomuz+wVUrlNhZeE4pEyxC2InjJvdQEmYRz1SCIrhqwy59lmJZ3h+Z8uLyFbk3zjYysrv4glxvWWIsK0CSLcHhpqrdw6HDjyZUHQVMEfoVxW5UXLYxnO0KDaLd00Db+G5wey4iKdIP4CpHSLfagtGoaoQ792sF1huSX2Kfaf1tbmrHXY7SQCFgLwp4u549IMFl/KYGkiv54H+ocuI7FjacNdMSf+Z9NFGvw5qoUWxFwZw==',
    'JSESSIONID': 'ECCDFCCD3DC1F69EED766B9E259A7248',
    'session-id': '257-8092929-3802430',
    'x-acbfr': '"2WlLDVOV4@rflJ8CWbWrRTW@WYMC7CuXs6ABH0C5gStr@V0vQwjKDJEvpEepoKBI"',
    'at-acbfr': 'Atza|IwEBIFNvjmDd08iu3lmiKRsBGzXu4pS83J8ykf5kZfzhm-IvOhqDIzXTOBLL64i_lC472sQ69ttNJV2H6F9jdmiaAOXPYmwBzp3i1eg44nv8BjmLqGyHZT2Fvt1Xc5qbJ3ScBU6I-y3-3SqW0MlLMAEhqpKb2f_86nVSLRLiFeaO8O8EvAmlzySAXamDsi-PcMfgj84kSBy5GL3U8O5ApJA7cn-CrgtseDinDEU9JDaJz5fdbg',
    'sess-at-acbfr': '"56Ck6CmDPaLA9GCMui0PBhyym0ODTHf8WL6LQaChuig="',
    'session-id-time': '2082787201l',
    'session-token': '0uoTsTCbCjUyL1bKwp6LnoR3T3JeJ1RQYP+SSFJpNIcGE0OUpHWbY2M7zKzytem9++UGs0/JKPq1tCkhpjm9dU3oF6J+PdOhN3JWZ2z7M2wkl5bhnAFruZjwAvZLhtfIWRLcujJC/7bQjUXFsKaOmvYtlcT6sbGmLaT4uVSGsGbCMBZkLh4wrecuZp6bSWzN3EJfdzUjlQ0D+dp36ShVMXGMtUyZu18LfhVBSPLo+a4WcqHYOjNRG0Nn3TddZwjVpCxKEBOXgzkM8zS00ELBddhE5XwTUcZBiAmSxKRE5U9WOmJuP4XnMNXm41YedFGYxpYAaUYElr7xqUAFE8Mb5Jh6RreT56lfdcP3ukzXV3Q',
    'bm_sv': '667C0B09BBF87E087F1EB9F1D17E2915~YAAQxNhLFwqBxriQAQAAibn5uxgE+bAjdAxFYqb+Cd/l3QXMVHJGsL2xwZ1s+ymUBj3iWgta+vV7nQUa2m9Yxa5YUjn+MpAZMoSWTzFfflzpMLZ7GZb7pRjE3aM/Db6TGq4QElEU2Sd4Q+qG2o9FeA+prds7gqnnBDwSU30rRYdbmd2JY+Jl9tN/5wk731mzjTL9217SO2NHs0wGCHkxtEJ4AU+SQRaxqj/WcYU9CAj/zOg7k2H38ngQ++J8OjzCEQ==~1',
    'cwr_s': 'eyJzZXNzaW9uSWQiOiIyNTM0NGY1Ny1kYmE1LTQ5MzAtYjI3Yy1jZWZmYjQ3ZGQzNDkiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjQxMCwicGFnZSI6eyJwYWdlSWQiOiIvb3BlcmF0aW9ucy9leGVjdXRpb24vcm91dGVzIiwicGFyZW50UGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL3JvdXRlcy82MjMwMzEwLTE2MCIsImludGVyYWN0aW9uIjozMjYsInJlZmVycmVyIjoiaHR0cHM6Ly9sb2dpc3RpY3MuYW1hem9uLmZyL2RzcGNvbnNvbGU/c3RhdGlvbj1EV1AxJmNvbXBhbnlJZD05ZjQzMWQ3Mi1iNzVlLTQ2YTktYTQ5YS03NWFhOTkyODNiNzcmcGFnZUlkPWRzcF9iaGQmdGFiSWQ9YmhkLWRzcC10YWImdGltZUZyYW1lPURhaWx5JnRvPTIwMjQtMDctMTYiLCJyZWZlcnJlckRvbWFpbiI6ImxvZ2lzdGljcy5hbWF6b24uZnIiLCJzdGFydCI6MTcyMTE0MDgzMzE2M319',
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

    st.title("Amazon Client pour MASSI")

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
