import streamlit as st
import pandas as pd
from utils import *
import requests
from configure import auth_key
from time import sleep
import json

## Set session state
if 'start_point' not in st.session_state:
    st.session_state['start_point'] = 0

def update_start(start_t):
    st.session_state['start_point'] = int(start_t / 1000)

st.title("Audit a YT channel")
st.caption("With this app you can audit a YT channel to see if you'd like to sponsor them")

file = st.file_uploader('Upload a file that includes the video links')
if file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(file, header=None)

    list = dataframe[0].tolist()

    video_url = st.selectbox("Select a video to analyze", list)

    video_title, save_location = save_audio(video_url)

    st.write(list[0])

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": video_url,
        "auto_chapters": True
    }
    headers = {
        "authorization": auth_key,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    print(response.json())

    st.header(video_title)
    st.audio(save_location, start_time=st.session_state['start_point'])

    polling_endpoint = upload_to_AssemblyAI(save_location)


    ## Waiting for transcription to be done
    status = 'submitted'
    while True:
        polling_response = requests.get(polling_endpoint, headers=headers)
        transcript = polling_response.json()['text']
        status = polling_response.json()['status']

        if status == 'submitted' or status == 'processing':
            print('not ready yet')
            sleep(10)

        elif status == 'completed':
            print('creating transcript')

            # print(json.dumps(polling_response.json(), indent=4, sort_keys=True))

            # Display summaries
            chapters = polling_response.json()['chapters']
            chapters_df = pd.DataFrame(chapters)
            chapters_df['start_str'] = chapters_df['start'].apply(convertMillis)
            chapters_df['end_str'] = chapters_df['end'].apply(convertMillis)

            st.subheader('Summary notes from this meeting')
            for index, row in chapters_df.iterrows():
                with st.expander(row['gist']):
                    st.write(row['summary'])
                    st.button(row['start_str'], on_click=update_start, args=(row['start'],))

            break
        else:
            print('error')
            break