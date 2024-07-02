import requests
import json
import streamlit as st


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
    rates = {}
    for route_url in prefixed_route_ids:
        route_data = fetch_route_data(route_url, headers)
        if route_data:
            rate = calculate_mailbox_delivery_rate(route_data)
            route_id = route_url.split('/')[-1]  # extract route_id from route_url
            route_prefix = route_id.split('-')[0]  # extract prefix from route_id
            route_id_without_prefix = route_id.replace(f"{route_prefix}-", "")  # remove prefix from route_id
            rates[route_id_without_prefix] = f"{rate:.2%}"
    return rates


def search_amazon_data(local_date):
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
        'cwr_s': 'eyJzZXNzaW9uSWQiOiJhOTBjYWQ5NC0zYzZlLTRlOGItYWIzOC1hOGEwNGI4ZTFhZDUiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjI2NTYsInBhZ2UiOnsicGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL2l0aW5lcmFyaWVzIiwicGFyZW50UGFnZUlkIjoiL29wZXJhdGlvbnMvZXhlY3V0aW9uL3JvdXRlcyIsImludGVyYWN0aW9uIjo5MCwicmVmZXJyZXIiOiJodHRwczovL2xvZ2lzdGljcy5hbWF6b24uZnIiLCJzdGFydCI6MTcxNjg4ODczMTI1Mn19',
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
        st.header("Mailbox Delivery Rates")
        st.subheader(f"Date: {local_date}")
        st.write("")

        # Create a table to display the results
        table_data = []
        for route_id, rate in delivery_rates.items():
            table_data.append([route_id, rate])

        st.table(table_data)

    else:
        st.error(f"Failed to retrieve data: {response.status_code}")


# Streamlit UI
st.title("Amazon Logistics Mailbox Delivery Rates")
local_date = st.text_input("Enter local date (YYYY-MM-DD):", "2024-07-02")
if st.button("Search"):
    search_amazon_data(local_date)
