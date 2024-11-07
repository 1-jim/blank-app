import streamlit as st
import time
import requests
import pandas as pd

# adapted API calls from Eric https://github.com/BackupNerd/Backup-Scripts/blob/master/M365/GetM365DeviceStatistics.v31.ps1
ENUMERATEPARTNERS_FIELDS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]

API_URL = "https://api.backup.management/jsonapi"

def login(partner, username, password):
    """Authenticate and retrieve a visa token with 15-minute validity."""

    # Define the JSON payload for login
    data = {
        "jsonrpc": "2.0",
        "id": username,
        "method": "Login",
        "params": {
            "partner": partner,
            "username": username,
            "password": password
        }
    }
    
    try:
        # Send the login request
        response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        # Parse response and extract visa token
        result = response.json()
        
        if 'error' in result:
            raise Exception(f"Login error: {result['error']['message']}")
        
        data = result['result']['result']

        # Set visa expiration to current time + 15 minutes (900 seconds)
        st.session_state['VisaExpires'] = time.time() + 900

        print("Login successful, visa token obtained.")
        st.session_state['PartnerId'] = data['PartnerId']        
        st.session_state['VisaToken'] = result['visa']

        return result['visa'], data['PartnerId'] 

    except requests.RequestException as e:
        raise Exception(f"Network error during login: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during login: {e}")

def get_authentication():
    """Get a valid visa token, refreshing it if expired."""
    if not 'VisaToken' in st.session_state:
        st.session_state['VisaToken'] = None

    if 'VisaExpires' in st.session_state:
        visa_expiration = st.session_state['VisaExpires']
    else:
        visa_expiration = 0

    partner = st.session_state['CoveAccount']
    username = st.session_state['CoveUser']
    password = st.session_state['CoveUserPwd']

    # Check if visa token exists and is still valid
    if st.session_state['VisaToken'] is None or time.time() > visa_expiration or 'PartnerId' not in st.session_state:
        print("Visa token is expired or not available, re-authenticating...")
        return login(partner, username, password)
    else:
        print("Using cached visa token.")
        return st.session_state['VisaToken'], st.session_state['PartnerId']

def call_api_method(method_name, params):
    """Call a method on the API using the current visa token."""

    if not 'VisaToken' in st.session_state:
        get_authentication()

    if st.session_state['VisaToken'] is None:
        print("Failed to authenticate; cannot call API.")
        return

    # Define the JSON payload for the API method
    data = {
        "jsonrpc": "2.0",
        "id": 'auth',
        "visa": st.session_state['VisaToken'],
        "method": method_name,
        "params": params
    }

    try:
        # Send the API request
        response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        # Parse and return response data
        result = response.json()
        
        if 'error' in result:
            print(f"API Error: {result['error']['message']}")
            return None
        
        return result['result']
    except requests.RequestException as e:
        raise Exception(f"Network error during API call: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during API call: {e}")

def call_billing(customer):

    params = {"query" : {
    "PartnerId" : customer['Id'],
    "Totals": ["SUM(TM)"]}
    }

    json_data = {
        "jsonrpc": "2.0",
        "id": f"{customer['Id']}",
        "visa": st.session_state['VisaToken'],
        "method": "EnumerateAccountStatistics",
        "params": params
    }

    try:
        # Send the API request
        response = requests.post(API_URL, json=json_data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        # Parse and return response data
        result = response.json()
        
        if 'error' in result:
            print(f"API Error: {result['error']['message']}")
        
        return result
    except requests.RequestException as e:
        raise Exception(f"Network error during API call: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during API call: {e}")

def process_billing_customers():

    #session variables for the token etc
    try:
        partner = st.session_state['CoveAccount']
        username = st.session_state['CoveUser']
        password = st.session_state['CoveUserPwd']
    except:
        st.warning('Session Variable Error in Customer Billing Pre-Auth!')
        st.write(partner)
        st.write(username)
        st.write(password)
        st.stop()

    # First, log in to obtain and cache the visa token
    print("Logging in to obtain visa token...")
    get_authentication()

    #session variables for the token etc
    try:
        partner_id = st.session_state['PartnerId']
        token = st.session_state['VisaToken']
    except:
        st.warning('Session Variable Error in Customer Billing Post-Auth!')
        st.write(partner)
        st.write(username)
        st.write(password)
        st.stop()

    # Enumerating customers
    partner_id = st.session_state['PartnerId']
    partner_body = {
        'parentPartnerId': int(partner_id),
        'fields': ENUMERATEPARTNERS_FIELDS,
	    'fetchRecursively': False
    }

    partner_response = call_api_method('EnumeratePartners', partner_body)
    #st.write(partner_body, partner_response)
    if not partner_response:
        st.error('Error with Partner Response')
        st.stop()

    partner_result = partner_response['result']
    customer_list = []
    
    sorted_data = sorted(partner_result, key=lambda x: x['Name'])
    total_items = len(sorted_data)
    progress = 0
    
    for item in sorted_data:
        #feedback
        progress = progress + 1
        if (progress / total_items * 100) in [1,10,20,30,40,50,60,70,80,90]:
            st.toast(f"{int(progress / total_items * 100)}% Complete - Processing {item['Name']}", icon='✅',)

        customer = {
            "Id": item['Id'],
            "Name": item['Name'],
            "ParentId": item['ParentId'],
            "Level": item['Level'],
            "BillableM365Users": 0
        }

        billing_response = call_billing(customer)
        if not billing_response:
            print(f"API Error: BILLING RESPONSE IS EMPTY FOR {customer['Name']}")

        totals = billing_response['result']
        if totals:
            customer['BillableM365Users'] = totals['totalStatistics'][0].get('SUM(TM)')
            customer_list.append(customer)

    #format and return results
    df = pd.DataFrame(customer_list,columns=['Id','Name','ParentIdRemove','Level','BillableM365Users'])
    df_customers = df.drop('ParentIdRemove', axis=1)
    return df_customers