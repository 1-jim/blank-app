import time
import streamlit as st
from streamlit_option_menu import option_menu
from components.footer import show_footer
from features.Introduction import show_intro
from features.CustomerInfo import show_customers
from features.About import show_about

banner_height = 100

def mainMenu():
    st.logo('./media/utility.png',size='Large')
    c1 = st.container(border=0)
    with c1:
        col1, col2 = st.columns([2,4],vertical_alignment='top')
        with col1:
            with st.container(height=banner_height,border=0):
                col3, col4 = st.columns([1,6],vertical_alignment='center')
                col3.image(st.secrets.application.VENDOR_ICON,use_container_width=True)
                col4.markdown('**Cove** Data Protection')

        col2.image(st.secrets.application.MAIN_BANNER, use_container_width=True)

    with st.sidebar:
        welcomeMsg = f"Welcome {st.session_state['username']}!"
        st.session_state['menu_option'] = option_menu(
            welcomeMsg, ['Home', 'M365 User Billing', 'About'], 
            icons=['house', 'search', 'question'], 
            menu_icon="lock",
            default_index=0,
            orientation="vertical")
        
        c1 = st.container(border=0, height=300)
        col1,col2,col3 = st.columns([1,10,1], vertical_alignment='bottom')
        col2.code('BackupVault 2024 v0.1')
            
    match st.session_state['menu_option']:
        case 'Home':
            show_intro()
        case 'M365 User Billing':
            show_customers()
        case 'About':
            show_about()
        case _:
            show_about()

    show_footer()