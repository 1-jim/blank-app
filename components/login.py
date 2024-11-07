import streamlit as st
import os

def cove_login():
    env_tenant = os.getenv('CUSTOMER_NAME',None)
    if env_tenant:
        tenant = st.text_input('Tenant Name', value=env_tenant)
    else:
        tenant = st.text_input('Tenant',placeholder='Blueraq Networks Ltd (rob@backupvault.co.uk)')
    user = st.text_input('username',placeholder='your cove login that has API access')
    pwd = st.text_input('password',type='password',placeholder='your cove login passsword')

    creds = {
        'Tenant': tenant,
        'User': user,
        'Password': pwd
    }
    return creds