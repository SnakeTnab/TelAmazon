import requests
import json
import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit import caching


# Fetch data from the provided route URL
def fetch_route_data(route_url, headers):
    try:
        response = requests.get(route_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data for {route_url}: {e}")
        return None


# Calculate the delivery rate to mail slots
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


# Process each route, fetch data, and calculate delivery rates
def process_routes(prefixed_route_ids, headers):
    rates = []
    for route_url in prefixed_route_ids:
        route_data = fetch_route_data(route_url, headers)
        if route_data:
            rate = calculate_mailbox_delivery_rate(route_data)
            route_id = route_url.split('/')[-1]  # extract route_id from route_url
            route_prefix = route_id.split('-')[0]  # extract prefix from route_id
            route_id_without_prefix = route_id.replace(f"{route_prefix}-", "")  # remove prefix from route_id
            rate_str = f"{rate:.2%}".replace('.', ',')  # Convert the rate to a string
            rates.append([route_id_without_prefix, rate_str])
    return rates


# Fetch Amazon data based on the selected date
def search_amazon_data(local_date):
    cookies = {
        # Cookies content (consider securing sensitive data)
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

    try:
        with st.spinner('Fetching data...'):
            response = requests.get('https://logistics.amazon.fr/operations/execution/api/summaries',
                                    params=params, headers=headers)
            response.raise_for_status()

        data = response.json()
        all_route_ids = [route['routeId'] for itinerary in data['itinerarySummaries']
                         for route in itinerary['routes']]
        prefixed_route_ids = [f"https://logistics.amazon.fr/operations/execution/api/routes/{route_id}"
                              for route_id in all_route_ids]

        # Process each route and calculate mailbox delivery rates
        delivery_rates = process_routes(prefixed_route_ids, headers)

        # Display results using Streamlit
        st.header("Mailbox Delivery Rates")
        st.subheader(f"Date: {local_date}")
        st.write("")

        # Create a DataFrame to display the results
        df = pd.DataFrame(delivery_rates, columns=["Route", "Rates"])

        # Add conditional formatting
        st.dataframe(df.style.applymap(lambda x: 'background-color: green' if ',' in x and float(x.replace(',', '.').strip('%')) > 50 else 'background-color: red'), width=800, height=600)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")


# Streamlit UI
st.title("TNAB MAILSLOT")
local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))

# Cache the fetched data to improve performance
if st.button("Analyze"):
    caching.clear_cache()  # Clear cache to fetch fresh data each time
    search_amazon_data(local_date)
