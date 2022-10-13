import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sensitive content",
    page_icon="🚨",
)

print(st.session_state['content_moderation'])

if st.session_state['content_moderation']['summary'] != {}:
    st.header('🚨 Mention of the following sensitive topics detected.')
    moderation_df = pd.DataFrame(st.session_state['content_moderation']['summary'].items())
    moderation_df.columns = ['topic','confidence']
    st.dataframe(moderation_df, use_container_width=True)
else:
    st.header('✅ All clear! No sensitive content detected.')
