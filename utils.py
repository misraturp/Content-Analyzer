import streamlit as st
from pytube import YouTube
import os
import requests
from configure import auth_key
import pandas as pd
from time import sleep

## AssemblyAI endpoints and headers
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = "https://api.assemblyai.com/v2/upload"

headers = {
	"authorization": st.secrets["auth_key"],
	# "authorization": auth_key,
   "content-type": "application/json"
}

@st.cache
def get_links(file):
    print(st.session_state['file'])
    dataframe = pd.read_csv(st.session_state['file'], header=None)
    dataframe.columns = ['video_url']
    list = dataframe["video_url"].tolist()

    titles = []
    locations = []
    thumbnails = []

    for video_url in list:
        video_title, save_location, thumbnail_url = save_audio(video_url)
        titles.append(video_title)
        locations.append(save_location)
        thumbnails.append(thumbnail_url)

    dataframe['video_title'] = titles
    dataframe['save_location'] = locations
    dataframe['thumbnail_url'] = thumbnails

    return dataframe

@st.cache
def save_audio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    os.rename(out_file, file_name)
    print(yt.title + " has been successfully downloaded.")
    print(file_name)
    return yt.title, file_name, yt.thumbnail_url


## Upload audio to AssemblyAI
@st.cache
def upload_to_AssemblyAI(save_location):
	CHUNK_SIZE = 5242880

	def read_file(filename):
		with open(filename, 'rb') as _file:
			while True:
				print("chunk uploaded")
				data = _file.read(CHUNK_SIZE)
				if not data:
					break
				yield data

	upload_response = requests.post(
		upload_endpoint,
		headers=headers, data=read_file(save_location)
	)
	print(upload_response.json())

	audio_url = upload_response.json()['upload_url']
	print('Uploaded to', audio_url)


	## Start transcription job of audio file
	data = {
		'audio_url': audio_url,
		'auto_chapters': True,
		'iab_categories': True,
		'content_safety': True
	}

	transcript_response = requests.post(transcript_endpoint, json=data, headers=headers)
	print(transcript_response)

	transcript_id = transcript_response.json()['id']
	polling_endpoint = transcript_endpoint + "/" + transcript_id

	print("Transcribing at", polling_endpoint)
	return polling_endpoint

@st.cache
def get_results(dataframe, clicked, save_location):

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
			content_moderation = polling_response.json()["content_safety_labels"]
			topic_labels = polling_response.json()["iab_categories_result"]
			
			chapters_df = pd.DataFrame(chapters)
			chapters_df['start_str'] = chapters_df['start'].apply(convertMillis)
			chapters_df['end_str'] = chapters_df['end'].apply(convertMillis)

			return chapters_df, content_moderation, topic_labels

			break
		else:
			print('error')
			break


def convertMillis(start_ms):
	seconds = int((start_ms / 1000) % 60)
	minutes = int((start_ms / (1000 * 60)) % 60)
	hours = int((start_ms / (1000 * 60 * 60)) % 24)
	btn_txt = ''
	if hours > 0:
		btn_txt += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
	else:
		btn_txt += f'{minutes:02d}:{seconds:02d}'
	return btn_txt