import streamlit as st
import os
import locale
from features.Menu import mainMenu

st.set_page_config(page_title="Proof of Concept App", layout="wide")

locale.setlocale( locale.LC_ALL, '')

st.session_state['menu_option'] = 'Home'
st.session_state['username'] = os.getenv('USER_NAME','UNKNOWN!')
st.session_state['customername'] = os.getenv('CUSTOMER_NAME','CUSTOMER_NAME !MISSING!')

mainMenu()