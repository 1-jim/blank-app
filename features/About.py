import streamlit as st
from components.custom_mermaid import show_mermaider

button_disabled = False

def show_about():
    mermaid_code = """flowchart LR
    A[(Lots of data)] --> |Add to Model| B((fa:fa-brain AI MODEL))
    B <--> |cycle|C[(fa:fa-desktop System)]
    C <-->|cycle| D[fa:fa-user UI/UX]
    """
    show_mermaider(mermaid_code)
    st.divider()
