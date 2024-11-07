import streamlit as st

def show_footer():
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.divider()
    left_co, cent_co,last_co = st.columns(3)
    cent_co.image(f'{st.secrets.application.MAIN_BANNER}',width=200)
