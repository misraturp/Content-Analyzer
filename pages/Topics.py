import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Topic labels",
    page_icon="🚀",
)

st.title('The following topics are discussed in this video 👇')

if st.session_state['topic_labels'] != None:
    topics_df = pd.DataFrame(st.session_state['topic_labels']['summary'].items())
    topics_df.columns = ['topic','confidence']
    topics_df["topic"] = topics_df["topic"].str.split(">")
    topics_df[['high-level topic','sub-topic','main-topic']] = pd.DataFrame(topics_df.topic.tolist(), index= topics_df.index)
    topics_df = topics_df.drop('topic', axis=1)
    # topics_df = topics_df.groupby(['high-level topic', 'sub-topic', 'main-topic']).confidence.sum().to_frame()
    topics_df = topics_df.set_index(['high-level topic', 'sub-topic', 'main-topic']).sort_values(['confidence'], ascending=False)
    print(topics_df)
    st.dataframe(topics_df, use_container_width=True)