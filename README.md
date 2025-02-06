# Hack The Bottle Project 

This project is a system to play YouTube videos on a local WiFi network and log which videos are played. The goal of this system is to 'infect' the algorithms of other devices on the network with specific content for the purposes of disrupting information filter bubbles. 

## Files 

Originally we were using an ESP32 with Arduino, but have switched to using a Raspberry Pi 5 with Python. Below is a key to understand what the files in this project. 

| File          | Purpose       | Current       |
| ------------- | ------------- | ------------- |
| publish2GSheet.py | Python for publishing data to a Google Sheet - contains update_sheet function | yes |
| HACK-WIFI-1.ino   | Arduino for listing YouTube videos                                            | no  |
| Publish2Sheet_2_noAPI.ino     | Arduino for publishing data to a Google Sheet                     | no  |
| To Run A Playlist Of Video    | ?? | ?  |
| To Run One Video On Raspberry | ?? | ?  |