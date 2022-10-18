# How to make a video content analyser!
My name is Mısra Turp and I work as a developer educator at AssemblyAI. As part of our marketing, we work with many online creators. Even though it’s fun to make new connections and get to know new creators in this field, it is not always easy to make sure that the content matches our criteria. Looking through the videos of a channel gets time-consuming and even then we might miss something.

For this, I have made an app using Streamlit and AssemblyAI’s API in order to automatically analyse a given channel’s content.

In this post you’ll learn how to:
* Use AssemblyAI’s API to analyze video content
* Use multiple pages to present results
* Use a custom Streamlit component

**Shortcut:** “Want to jump right in? Here’s  [the content analyzer on Streamlit Share](link)  and a  [Github repo with all the code](https://github.com/misraturp/Content-Analyzer) .”

This app consists of three pages. 
On the main page, we will collect the input from the user and visualize the thumbnails of the videos to be selected.
On the other two pages, the user will be able to view, the topics covered in the selected video and whether there was any harmful language involved.

Before we get started, what you need for this project are a couple of Python libraries and an AssemblyAI API key. You can get the API key for free through assemblyai.com by creating a free account. And make sure you have:
* Streamlit
* Pandas
* Requests
* Pytube
libraries installed. They can all be installed using pip install.

Once you have everything set up, we can start with building the main page.

## Step 1: Collect input from user
We will use file_uploader and ask the user to upload a txt file that includes links to a channel’s videos. Each link should be on a new line for ease of parsing later.
Once we get this list from the user, we will use the pytube library to download the audio of these videos. On top of the audio, pytube lets us collect the title and thumbnail information for this video.
And lastly, we need the user to select a video that they want to see analysis results for.
The easiest way to do this would be to show them a drop down list of all video’s titles. But humans are visual beings. So instead, showing them a scrollable list of thumbnails that they can click on to choose would be more user friendly.
This is not a native option on Streamlit but luckily, Streamlit user vivien, has made a custom component that displays images in a nice looking grid and makes them clickable.
Once we install this custom component, we can import it in our project and use this to get the user’s selection.
## Step 2: Get results from AssemblyAI
Now that we have all the input we need from the user, the next step is to pass the audio file of the selected video to AssemblyAI in order to get analysis results.
In this project, we are using 3 models from AssemblyAI. First one is the sumarization model that given an audio or video file, returns us a summary, if needed, divided into chapters. Second one is the content moderation model that can flag a given audio or video for including potentially sensitive content. If harmful content is found, it will return to us, what type of sensitive topics were included in this audio file. Some examples are: alcohol, violance, gambling, hare speech, etc. Lastly, we will use the topic detection mode, which is quite a self explanatory model that detects the topics that are discussed in a given audio or video file. There are nearly 700 topics that can be detected with the topic detection model which include: Automative, Business, Technology, Education and more granular version of these such as standardized tests, inflation, off-road vehicles and so on.

First step is to upload the audio file that we downloaded in the previous step to AssemblyAI. There is an upload end point for that, and we send this audio file by dividing it into chunks through the requests library by sending a post request. As a response, we get the url that this audio file is uploaded to.

Once that is done, the next step is to start the analysis. For this, we send another post request to AssemblyAI by specifying the location of the uploaded audio file, the analyses we want to get done.

As a response to this, we get an id for this job that has been started at AssemblyAI. The analyses takes a couple of minutes, depending on the length of the audio file. In the meantime, our app has to send get requests AssemblyAI to ask whether the analysis is done.

Once the results are ready, the next step is to parse them and display them to the user!
Firstly, we need to separate the three results. The summary, sensitive content detection and topic detection. All three will be sent to three different pages.
## Step 3: Present results
In the main page, we will show user the summaries right below the selected video’s title and the option to play the audio of this YouTube video.

The results of the model gives us a bunch of information. For each chapter, we have the gist of this chapter, a short headline and a summary of what is being discussed in a couple of sentences. We also have a timestamp in miliseconds of when this chapter starts and ends.
I use the Streamlit expander widget to show the summaries divided into chapters in a neat way. The title of each expander will be the gist of the chapter, and once expanded, it will show the full summary of the chapter. Bdelow the summary, I also included a button that points to the beginning of this chapter. Once clicked, it will jump the start of the audio playing widget to the beginning of this chapter, so that the use can listen the chapters themselves.

The results of the content moderation give us detailed information on which sentence caused this audio to be flagged, timestamp of when it start, when it ends, the severity of this sensitive topic and the confidence in this detection. This is all good and detailed information but for the purposes of this project we don’t need it to be this granular. Luckily, there is another section that is returned by the content moderation model which is the summary section that includes a summary of all this information. It tells us which sensitive topics were detected in this audio file and with what confidence. Pasting this information to a Pandas dataframe, we can easily show this data to the user.

What we get from the topic detection model is also quite similar. And again, I only used the summary results to make it easy for the user to understand. Once pasted into a Pandas dataframe, I structure this dataframe to have a separate column for each level of granularity of topics. And sort this topic list with the confidence AssemblyAI’s topic detection model detected them with.

## Wrap-up
And that’s it! It’s a bit of work but it is an app that makes analysing the videos of a youtube channel we recently came across very easy! And once you get the connection to AssemblyAi build up, there are many other apps you can make this Streamlit. You can check out the documentation of AssemblyAI to figure out what other models we offer and how to use them to get more information out of your audio or video files.

If you have any questions about this app or if you build an app of your own using AssemblyAI and Streamlit let us know though Twitter or YouTube!








