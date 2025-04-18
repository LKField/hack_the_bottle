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
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.activities().list(
        part="id, snippet, contentDetails",
        home=True
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()

