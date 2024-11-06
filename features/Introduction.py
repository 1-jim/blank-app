import streamlit as st

def show_intro():
    st.markdown('## Customer Account Management')
    st.markdown('### Application Features')
    st.info('Collection of Partners within Cove Backup Environment')
    st.info('Interrogation of Customer Counts within each Partner for Billing changes')
    st.info('Creation of a CSV output for Finance team processing')
    st.divider()
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(f'{st.secrets.application.MAIN_BANNER}',width=200) 

    


