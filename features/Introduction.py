import time
import streamlit as st

def show_intro():
    st.markdown('## Customer Account Management')
    message = st.chat_message("assistant")
    time.sleep(1)
    message.write(f"Hello {st.session_state['username']}")
    time.sleep(1)
    message.write('A new feature is the abillity to extract M365 user totals for each customer.')
    message.write('Check it out in the sidebar menu.')
    message.divider()

    st.markdown('### Application Features')
    st.info('Collection of Partners within Cove Backup Environment')
    st.info('Interrogation of Customer Billing Data within each Partner to identify latest changes')
    st.info('Creation of a formatted file output for Finance team processing')
