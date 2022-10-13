import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Topic labels",
    page_icon="🚀",
)

topics_df = pd.DataFrame(st.session_state['topic_labels']['summary'].items())
topics_df.columns = ['topic','confidence']
st.dataframe(topics_df, use_container_width=True)