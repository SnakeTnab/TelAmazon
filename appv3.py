import streamlit as st
import requests
import json
from datetime import datetime
import urllib.parse
import concurrent.futures

# Mise en cache des données
@st.cache_data
def fetch_route_data(route_link, cookies):
    """Récupère les données d'une route spécifique."""
    try:
        response = requests.get(route_link, cookies=cookies)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            st.error(f"Échec pour l'URL {route_link} (Code : {response.status_code})")
    except Exception as e:
        st.error(f"Erreur lors de la récupération de {route_link} : {e}")
    return None


@st.cache_data
def search_amazon_data(local_date):
    """Récupère toutes les données des routes pour une date donnée."""
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
    'bm_sv': '68E5CF70457B9B56DC026F3AD12854E3~YAAQz9hLF8DGqf+QAQAANXa1JxheDtWgBQ1Iho3Tz2tMP46EcsN5F2eZMC/ruflkOK8KdgPT5lNHHoTfGHWo1E7GzwXxkaapLCazbp0QuP2qQEZi3bPePiMhoZ7ugmsx8OUmef5tXkS+iSXsDd9ACmbR9ToVe/lv8w6X7D+3Yh1InKyqJdI3/RhNkvelwaZuNnBo9ixj1hxioY1HJJWuOmcSCkM6uNG0cAt3kFMys6RgNBsxmyzPrwCdJAzMbeI=~1',
    'session-id': '258-3085241-4888146',
    'session-token': 'XCshqmMy2tEksfNzi0AOmv+If8ug67KKfsLdr4vu1bE5PPX8TR8meQujgZ5efPEEMegesYZsQFr8DXOITAd2shjCa/gSNVDE5/ZqwaTlfGXhmvtbr0Txfh36FzmMIedK42wAOXdZ/NwgMgbjVvdLZjU73diLYTOnXGeMkgzKetQl1Pc501bwxsUZIuUeIG5pIgyEbM9C4+xIc9vhyJYYq/3cdfLUtq3F4cHjPX3pLtuvtOCWoF5eY8ItHdTAGEYFMO6JzyXDuCCnBJ3vGrV8ajw5ZbBno48WiyqTl5gpvE6uOWkyro5YlKFxUrYsPYAhoxhCUloxqJ4B5fau7j7bKc/waYRcK3ehdvErBZcS0VQ',
    'cwr_s': 'eyJzZXNzaW9uSWQiOiIyYmQxMGU2MS1jMzY2LTQzMzUtYWIzOC00NGI4MTE0MWFjZjEiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjI0OTMsInBhZ2UiOnsicGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL2l0aW5lcmFyaWVzIiwicGFyZW50UGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL3JvdXRlcyIsImludGVyYWN0aW9uIjoxMzEsInJlZmVycmVyIjoiaHR0cHM6Ly9sb2dpc3RpY3MuYW1hem9uLmZyL2FjY291bnQtbWFuYWdlbWVudC9kZWxpdmVyeS1hc3NvY2lhdGVzP3Byb3ZpZGVyVHlwZT1EQSZwcm92aWRlclN0YXR1cz1PTkJPQVJESU5HJnNlYXJjaFN0YXJ0PTAmc2VhcmNoU2l6ZT0xMDAiLCJyZWZlcnJlckRvbWFpbiI6ImxvZ2lzdGljcy5hbWF6b24uZnIiLCJzdGFydCI6MTcyMjk0ODQyODAyNn19',
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

        # Récupérer les données en parallèle
        all_route_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(fetch_route_data, route_link, cookies): route_link for route_link in prefixed_route_ids}
            for future in concurrent.futures.as_completed(future_to_url):
                route_data = future.result()
                if route_data:
                    all_route_data.append(route_data)

        return all_route_data
    else:
        st.error("Échec de la récupération des données logistiques Amazon.")
        return None


def extract_all_scannable_ids(route_data_list):
    """Extrait tous les scannableId et leurs informations associées."""
    return [
        {
            'scannableId': package['scannableId'],
            'name': stop['stopDetails']['address']['name'],
            'address1': stop['stopDetails']['address']['address1'],
            'address2': stop['stopDetails']['address'].get('address2', ''),
            'postalCode': stop['stopDetails']['address']['postalCode'],
            'city': stop['stopDetails']['address']['city'],
            'phone': stop['stopDetails']['address'].get('phone', '')
        }
        for route_data in route_data_list
        for stop in route_data['routePlan']['stopList']
        for package in stop['stopDetails']['packageList']
    ]


def share_on_whatsapp(result):
    """Crée un lien pour partager les informations sur WhatsApp."""
    message = f"Nom: {result['name']}\nAdresse 1: {result['address1']}\nAdresse 2: {result['address2']}\nCode postal: {result['postalCode']}\nVille: {result['city']}\nTéléphone: {result['phone']}"
    whatsapp_link = f"https://wa.me/?text={urllib.parse.quote_plus(message)}"
    return whatsapp_link


def main():
    # Définir l'icône de la page avec un emoji téléphone
    st.set_page_config(page_icon="📞", page_title="Amazon Client")

    st.title("Amazon Client")

    local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))

    if st.button("Rechercher"):
        formatted_date = local_date.strftime("%Y-%m-%d")
        
        # Mesurer le temps de récupération des données
        with st.spinner("Récupération des données..."):
            route_data_list = search_amazon_data(formatted_date)

        if not route_data_list:
            st.warning("Aucune donnée de route trouvée.")
        else:
            st.success("Données récupérées avec succès.")
            
            # Extraction des scannable IDs
            scannable_ids = extract_all_scannable_ids(route_data_list)

            if not scannable_ids:
                st.warning("Aucun scannableId trouvé.")
            else:
                for result in scannable_ids:
                    st.write("Scannable ID :", result['scannableId'])
                    st.write("Nom :", result['name'])
                    st.write("Adresse 1 :", result['address1'])
                    st.write("Adresse 2 :", result['address2'])
                    st.write("Code postal :", result['postalCode'])
                    st.write("Ville :", result['city'])
                    st.write("Téléphone :", result['phone'])
                    st.write("-" * 30)

                    # Lien WhatsApp
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
