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
                if package.get('trObjectReason') == "DELIVERED_TO_MAIL_SLOT":
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
        st.header("les taux de livraison en boites au lettres")
        st.subheader(f"Date: {local_date}")
        st.write("")

        # Create a DataFrame to display the results
        import pandas as pd
        df = pd.DataFrame(delivery_rates, columns=["Route", "Rates"])

        st.dataframe(df, width=800, height=600)

    else:
        st.error(f"Failed to retrieve data: {response.status_code}")


# Streamlit UI
st.title("TNAB MAILSLOT")
local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2038, 1, 1))
if st.button("Analyser"):
    search_amazon_data(local_date)
