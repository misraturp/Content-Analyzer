import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Topic labels",
    page_icon="🚀",
)

if st.session_state['topic_labels'] != None:
    st.title('The following topics are discussed in this video 👇')
    topics_df = pd.DataFrame(st.session_state['topic_labels']['summary'].items())
    topics_df.columns = ['topic','confidence']
    topics_df["topic"] = topics_df["topic"].str.split(">")
    expanded_topics = topics_df.topic.apply(pd.Series).add_prefix('topic_level_')
    topics_df = topics_df.join(expanded_topics).drop('topic', axis=1).sort_values(['confidence'], ascending=False).fillna('')

    st.dataframe(topics_df, use_container_width=True)
else:
    st.title('Once you select a video on the main page, you can see the topics here.')