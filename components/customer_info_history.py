from datetime import datetime
import os
import pandas as pd
import streamlit as st
import altair as alt

def show_customer_info_history():
    directory = st.session_state['data_directory']

    # Get filenames and sort them by modification time (latest first)
    filenames = sorted(
        [f for f in os.listdir(directory) if f.endswith('.csv')],
        key=lambda x: os.path.getmtime(os.path.join(directory, x)),
        reverse=True
    )

    st.title('Historic File Downloader')
    expand_chart = True
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        # Convert Unix timestamp to a readable date format
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        st.info(f"File: {filename} created on {mod_time}")
        col1,col2 = st.columns([2,3],vertical_alignment='bottom')
        c1 = col1.container(border=0)
        c2 = col2.container(border=0)
        # Create a text input for searching customer names
        search_query = c1.text_input(f"Search {filename}",placeholder='start typing a customer name')
        
        # Button to download the CSV file
        with open(filepath, 'rb') as f:
            c2.download_button(
                label=f"Download {filename}",
                data=f,
                file_name=filename,
                mime='text/csv',
                type='primary'
            )
        
        df = pd.read_csv(filepath)
        
        # Filter the dataframe based on the search query
        if search_query:
            filtered_df = df[df['Name'].str.contains(search_query, case=False, na=False)]
        else:
            filtered_df = df
               
        # Create a chart with the filtered dataframe
        levels = ["Reseller", "EndCustomer"]
        colors = ["#E66A5F","#0DE030"]
        chart = (
            alt.Chart(filtered_df)
            .mark_bar(opacity=0.7)
            .encode(
                x="BillableM365Users:Q",
                y=alt.Y("Name", stack=None),
                color=alt.Color(
                    field='Level',
                    type='nominal',
                    title='Level',
                    scale=alt.Scale(
                        domain=levels,
                        range=colors
                    )
                ),
                tooltip=['BillableM365Users:O','Name','Level'],
            )
        )
        
        ex_chart = st.expander(f'Data chart for {filename}',expanded=expand_chart)
        ex_chart.altair_chart(chart, theme='streamlit', use_container_width=True)
        
        ex_tbl = st.expander(f'Raw data within {filename}')
        ex_tbl.write(filtered_df)
        expand_chart = False
        st.divider()
    st.code('there are no more historic files')