import requests
import json
import streamlit as st
from datetime import datetime


def fetch_route_data(route_url, headers):
    response = requests.get(route_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve data for {route_url}: {response.status_code}")
        return None


def calculate_mailbox_delivery_rate(route_data):
    total_delivered = 0
    delivered_to_mail_slot = 0

    for stop in route_data.get('routePlan', {}).get('stopList', []):
        for package in stop.get('stopDetails', {}).get('packageList', []):
            if package.get('trObjectState') == "DELIVERED":
                total_delivered += 1
                if package.get('trObjectReason') == "DELIVERED_TO_SAFE_LOCATION":
                    delivered_to_mail_slot += 1

    if total_delivered == 0:
        return 0

    return delivered_to_mail_slot / total_delivered


def process_routes(prefixed_route_ids, headers):
    rates = []
    for route_url in prefixed_route_ids:
        route_data = fetch_route_data(route_url, headers)
        if route_data:
            rate = calculate_mailbox_delivery_rate(route_data)
            route_id = route_url.split('/')[-1]  # extract route_id from route_url
            route_prefix = route_id.split('-')[0]  # extract prefix from route_id
            route_id_without_prefix = route_id.replace(f"{route_prefix}-", "")  # remove prefix from route_id
            # Convert the rate to a string and replace the point with a comma
            rate_str = f"{rate:.2%}".replace('.', ',')
            rates.append([route_id_without_prefix, rate_str])
    return rates


def search_amazon_data(local_date):
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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'https://logistics.amazon.fr/operations/execution/',
        'Cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()]),
    }

    params = {
        'localDate': local_date,
        'serviceAreaId': 'd459788b-6a73-48f9-a713-81afa0c59b66',
    }

    response = requests.get('https://logistics.amazon.fr/operations/execution/api/summaries', params=params,
                            headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        all_route_ids = []

        for itinerary in data['itinerarySummaries']:
            route_ids = [route['routeId'] for route in itinerary['routes']]
            all_route_ids.extend(route_ids)

        prefixed_route_ids = [f"https://logistics.amazon.fr/operations/execution/api/routes/{route_id}" for route_id in
                              all_route_ids]

        # Process each route and calculate mailbox delivery rates
        delivery_rates = process_routes(prefixed_route_ids, headers)

        # Display results using Streamlit
        st.header("les taux de Capa Project")
        st.subheader(f"Date: {local_date}")
        st.write("")

        # Create a DataFrame to display the results
        import pandas as pd
        df = pd.DataFrame(delivery_rates, columns=["Route", "Rates"])

        st.dataframe(df, width=800, height=600)

    else:
        st.error(f"Failed to retrieve data: {response.status_code}")


# Streamlit UI
st.title("TNAB CAPA PROJECT")
local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))
if st.button("Analyser"):
    search_amazon_data(local_date)
