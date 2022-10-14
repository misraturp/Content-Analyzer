import streamlit as st
import pandas as pd
from utils import *
import requests
from configure import auth_key
from time import sleep
import json

## custom component = https://discuss.streamlit.io/t/custom-component-to-display-clickable-images/21604
from st_clickable_images import clickable_images

## Set session state
if 'start_point' not in st.session_state:
    st.session_state['start_point'] = 0
    st.session_state['selected_video'] = -1
    st.session_state['videos'] = []
    st.session_state['content_moderation'] = None
    st.session_state['topic_labels'] = None
    st.session_state['file'] = None

def update_start(start_t):
    st.session_state['start_point'] = int(start_t / 1000)

def update_file():
    st.session_state['file'] = st.session_state["uploaded_file"]

st.title("Analyze a YouTube channel's content")
st.markdown("With this app you can audit a Youtube channel to see if you'd like to sponsor them. All you have to do is to pass a list of links to the videos of this channel and you will get a list of thumbnails. Once you select a video by clicking its thumbnail, you can view:")
st.markdown("1. a summary of the video,") 
st.markdown("2. the topics that are discussed in the video,") 
st.markdown("3. whether there are any sensitive topics discussed in the video.")

st.file_uploader('Upload a file that includes the video links (.txt)', key="uploaded_file", on_change=update_file)

if st.session_state['file'] is not None:

    dataframe = get_links()
    st.session_state['videos'] = dataframe

    thumbnails_list = dataframe["thumbnail_url"].tolist()
    name_list = dataframe["video_title"].tolist()

    clicked = clickable_images(thumbnails_list,
    titles= name_list,
    div_style={"height": "400px", "display": "flex", "justify-content": "center", "flex-wrap": "wrap", "overflow-y":"auto"},
    img_style={"margin": "5px", "height": "150px"},
    key = "selected_image"
    )

    st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

    print(st.session_state['selected_image'])
    if clicked > -1:
        video_url = dataframe.loc[clicked]['video_url']
        video_title = dataframe.loc[clicked]['video_title']
        save_location = dataframe.loc[clicked]['save_location']

        st.header(video_title)
        st.audio(save_location, start_time=st.session_state['start_point'])

        chapters_df, content_moderation, topic_labels = get_results(dataframe, clicked, save_location)

        st.session_state['content_moderation'] = content_moderation
        st.session_state['topic_labels'] = topic_labels

        st.subheader('Summary notes from this video')
        for index, row in chapters_df.iterrows():
            with st.expander(row['gist']):
                st.write(row['summary'])
                st.button(row['start_str'], on_click=update_start, args=(row['start'],))

        clicked = -1
        status = 'submitted'