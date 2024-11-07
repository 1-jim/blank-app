import streamlit as st
from components.custom_mermaid import show_mermaider

button_disabled = False

def show_about():
    mermaid_code = """flowchart TD
    A[(fa:fa-lock Portal Login)] --> |Token Authentication| B[[fa:fa-question Customer Hierarchy]]
    B --> |Enumeration|C[(fa:fa-server Data Processing)]
    C -->|Tabular Data| D[fa:fa-file File Output]
    C -->|Data Aggregation|E[fa:fa-magnifying-glass-chart Visualisations]
    """
    
    c1,c2 = st.columns(2)
    c1.markdown('**M365 Customer Billing Workflow**')
    c1.markdown('Authentication is made with the API service and a Visa token is provided with a 15 minute lifetime. The identity of the account is provided with the token, which is then used for a subsequent API call to the **EnumeratePartners** method.')
    c1.markdown('End Customers and Reseller names and identities are stored transiently and each one is used to call the **EnumerateAccountStatistics** endpoint, with a query request to summarise the M365 Billing data into a single value.')
    c1.markdown('Feedback is provided visually on screen for the long running process. Once complete, data is sorted and provided as a file output.')
    c1.markdown('Additionally a visualisation is provided on screen to support the data extract.')
    with c2:
        st.session_state["mermaid_svg_height"] = 600
        show_mermaider(mermaid_code)