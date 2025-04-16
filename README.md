# Hack The Bottle Project 

This project is a system to play YouTube videos on a local WiFi network and log which videos are played. The goal of this system is to 'infect' the algorithms of other devices on the network with specific content for the purposes of disrupting information filter bubbles. 

## Files 

Originally we were using an ESP32 with Arduino, but have switched to using a Raspberry Pi 5 with Python. Below is a key to understand what the files in this project. 

| File          | Purpose       | Current       |
| ------------- | ------------- | ------------- |
| publish2GSheet.py | Python for publishing data to a Google Sheet - contains update_sheet function | yes |
| youtubeRecommends.py | Python for connecting to YouTube API                                       | yes |
| HACK-WIFI-1.ino   | Arduino for listing YouTube videos                                            | no  |
| Publish2Sheet_2_noAPI.ino     | Arduino for publishing data to a Google Sheet                     | no  |
| To Run A Playlist Of Video    | ?? | ?  |
| To Run One Video On Raspberry | ?? | ?  |


## Introduction
In this project, we designed a device capable of endlessly streaming YouTube videos without displaying or playing any sound. The goal is to potentially influence the video recommendation algorithm for users connected to the same Wi-Fi network. This system is discreetly hidden inside a bottle to remain unnoticed in public spaces.

## Objective
The main goals of this project were:
- Stream YouTube videos in the background (no display or sound).
- Play one or more videos continuously in a loop
- Automate the entire video-playing process.
- Observe whether these views are recognized and counted by YouTube.

## Development Steps
We first started trying to use the ESP32 to stream videos, but found it was better to use a Raspberry Pi. We had three different pieces of the project under development in parallel: video playback, data logging for analysis, and 3D modeling for the housing. 
### Arduino (ESP32) 
#### 1. Data Logging - Google Sheets API 
As a method to track the played videos to compare with the suggested videos on different accounts on the same Wi-Fi network, a data logging system was established using the Google Sheets API.
Modifying code created by K. Suwatchai (Mobizt), a connection to the Google Sheet was established and the data logging began. 

This was a good opportunity to learn about how to hide API keys and other sensitive information as well, although the pivot to Raspberry Pi happened before much progress could be made on that front. 
#### 2. Connecting to ESP32 - YouTube API 
Efforts were made to connect the ESP32 to video playback after a Wi-Fi connection was established. The following code in HACK-WIFI-1.ino was used to connect to the YouTube API and access the search function.
```
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "SPIFFS.h" // Pour enregistrer les résultats JSON dans un fichier
// Informations Wi-Fi
const char *ssid = "#";
const char *password = "#";
// Informations API YouTube
const char* apiKey = "#";
const char* searchQuery = "cats";
const int maxResults = 5;
```
After the initial setup of the structure and establishing the Wi-Fi connection, the intention was to connect to the YouTube API to access the search features so that we could play videos about a specific topic, returning the resulting links and information in a JSON. While this was successful, we soon realized  that the desired playback was not going to work on the ESP32 and we chose to pivot our attention to using a Raspberry Pi 5. 

### Raspberry Pi 5
#### 1. Connecting to the Raspberry Pi 5
The first challenge was connecting the Raspberry Pi to Wi-Fi. This turned out to be more difficult than expected due to connection instability. After many attempts at reconnecting and troubleshooting, we finally established a stable connection.
#### 2. Streaming Videos Without a Screen
Once connected, we tried streaming YouTube videos without using a screen. We used two tools:
yt-dlp: to extract the direct video stream URL
ffmpeg: to play the video stream without showing the video or playing any audio.
Installing Dependencies:
sudo apt update && sudo apt upgrade -y
sudo apt install yt-dlp ffmpeg -y
Single Video Streaming Script (play_video.py):
```py
import subprocess

youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your video URL

command_get_stream = ["yt-dlp", "-g", "-f", "best", youtube_url]

try:
    video_stream_url = subprocess.check_output(command_get_stream).decode().strip()

    command_play = [
        "ffmpeg", "-re", "-i", video_stream_url, "-f", "null", "-"
    ]

    subprocess.run(command_play)

except Exception as e:
    print("Error:", e)
```

Run the script:
python3 play_video.py
#### 3. Powering the Raspberry Pi with a Battery
We searched for a compatible battery for the Raspberry Pi 5. After some trials and research, we found the right one and got it working by following instructions found in the product’s datasheet.
#### 4. Connecting a Screen
To address the issue of uncounted views, we connected a display to the Raspberry Pi. This allowed us to:
Flash a fresh OS version with GUI support.
Monitor in real time what was happening on the Raspberry Pi.
#### 5. Streaming YouTube Videos with Display
With the screen connected, we used mpv (a video player) to stream YouTube videos in full screen, simulating a real view.
Playback Command:
```py
mpv --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" --fullscreen $(yt-dlp -f best -g <YOUTUBE_URL>)
```
#### 6. Automating the Loop Playback
To automate the entire process, we created a script to play a list of YouTube videos, with a 5-second pause between each.
Playlist Playback Script (auto_player.py):
```py
import subprocess
import time

video_playlist = [
    "https://www.youtube.com/watch?v=XQ0B0cjq1-U",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
    "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
]

def get_video_url(youtube_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-g", youtube_url],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Error retrieving link for {youtube_url}")
        return None

def play_videos(video_urls):
    for url in video_urls:
        print(f"Playing: {url}")
        video_stream_url = get_video_url(url)
        if video_stream_url:
            subprocess.run([
                "mpv",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "--fullscreen",
                video_stream_url
            ])
        print("Waiting 5 seconds before next video...\n")
        time.sleep(5)

if __name__ == "__main__":
    print(f"{len(video_playlist)} videos to play.")
    play_videos(video_playlist)
    print("Finished playing all videos.")    
```

#### 7. Data Logging - Google Sheets API 
As a method to track the played videos to compare with the suggested videos on different accounts on the same Wi-Fi network, a data logging system was established using the Google Sheets API.
With the switch to using Raspberry Pi, the work that was done on this front with the ESP32 had to be redone in python. Using code created by Allan Schwartz, with modifications, a link to a Google Sheet was established for data logging. Additionally, during this step, a method of hiding sensitive information such as the API key was used. 

#### 8. Recommendations - YouTube API 
Using the examples in the YouTube API, we tried to access the list of suggested videos, which would have allowed us to monitor the influence of our 'infection'. However, we ran into some challenges because of privacy protections implemented within the API. 
```py
# -*- coding: utf-8 -*-
# Sample Python code for youtube.activities.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
# THIS WILL NOT WORK AS IS ON THE PI - Requires access to website for verification (maybe as ssh this will be possible)
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
scopes = ["https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"]
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_tube.json"
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file            (client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    request = youtube.activities().list(part="id, snippet, contentDetails", home=True)
    response = request.execute()
    print(response)
if __name__ == "__main__":
    main() 
```

### Bottle - CAD
