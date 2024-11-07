import csv
import streamlit as st
from components.customer_info_history import show_customer_info_history
from components.login import cove_login
from features.About import show_about
from services.customer_billing import process_billing_customers
from datetime import datetime

def show_customers():
    button_disabled = False
    col1,col2 = st.columns([3,1])
    with st.container(border=1):
        with col1:
            credentials = cove_login()
            if credentials['Password']:
                st.session_state['CoveAccount'] = credentials['Tenant']
                st.session_state['CoveUser'] = credentials['User']
                st.session_state['CoveUserPwd'] = credentials['Password']

            ready = st.button("Fetch Billing Data",type='primary',use_container_width=True, icon='🔑',disabled=button_disabled)

    if ready:
        if 'billing_data' in st.session_state:
            del st.session_state['billing_data']

        button_disabled = True
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S").replace(' ','').replace('-','').replace(':','')
        st.session_state['billing_filename'] = f'cove_customer_data_{date_time_str}.csv'
        with st.spinner('collecting data'):
            df = process_billing_customers()
            if not df.empty:
                st.session_state['billing_data'] = df
        button_disabled=False

    if 'billing_data' in st.session_state and 'billing_filename' in st.session_state:
        dir_path = st.session_state['data_directory']
        filename = f"{dir_path}/{st.session_state['billing_filename']}"
        data = st.session_state['billing_data']
        with open(filename, 'w') as customer_file:
            data.to_csv(filename, sep=',',index=False,quoting=csv.QUOTE_ALL)

        # with open(filename) as f:
        #     st.download_button('Download CSV', f, file_name=filename)  # Defaults to 'text/plain'

    st.divider()
    show_customer_info_history()