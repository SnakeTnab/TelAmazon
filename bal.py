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
            rates.append([route_id_without_prefix, f"{rate:,2%}"])
    return rates


def search_amazon_data(local_date):
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
        st.header("les taux de livraison en boîte aux lettres")
        st.subheader(f"Date: {local_date}")
        st.write("")

        # Create a DataFrame to display the results
        import pandas as pd
        df = pd.DataFrame(delivery_rates, columns=["Route", "Rates"])

        st.dataframe(df, width=800, height=600)

    else:
        st.error(f"Failed to retrieve data: {response.status_code}")


# Streamlit UI
st.title("TNAB Mailbox Delivery")
local_date = st.date_input("Date :", min_value=datetime(2022, 1, 1), max_value=datetime(2025, 1, 1))
if st.button("Analyser"):
    search_amazon_data(local_date)
