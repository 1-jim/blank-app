import streamlit as st
from streamlit_option_menu import option_menu
from features.Introduction import show_intro
from features.CustomerInfo import show_customers
from features.About import show_about

banner_height = 100

def mainMenu():
    col1, col2 = st.columns(2,vertical_alignment='center')
    with col1:
        with st.container(height=banner_height):
            col3, col4 = st.columns([1,6],vertical_alignment='center')
            col3.image(st.secrets.application.VENDOR_ICON,width=40)
            col4.markdown('**Cove** Data Protection')

    col2.image(st.secrets.application.MAIN_BANNER, use_column_width=True)
    col2.markdown('#### Data Protection Experts')


    with st.sidebar:
        welcomeMsg = f'Hi {st.session_state["username"]}!'
        st.session_state['menu_option'] = option_menu(
            welcomeMsg, ['Home', 'Customers', 'About'], 
            icons=['house', 'search', 'question'], 
            menu_icon="lock",
            default_index=0,
            orientation="vertical")
            
    st.divider()
    match st.session_state['menu_option']:
        case 'Home':
            show_intro()
        case 'Customers':
            show_customers()
        case 'About':
            show_about()
        case _:
            show_about()