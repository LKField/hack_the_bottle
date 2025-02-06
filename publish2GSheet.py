# Original Author: Allan Schwartz
# Code Source: http://www.whatimade.today/log-sensor-data-straight-to-google-sheets-from-a-raspberry-pi-zero-all-the-python-code/

# Modified by: Lucretia Field 

# import many libraries
from __future__ import print_function  
from googleapiclient.discovery import build  
from httplib2 import Http  
from oauth2client import file, client, tools  
from oauth2client.service_account import ServiceAccountCredentials  
import datetime

# My Spreadsheet ID ... See google documentation on how to derive this
MY_SPREADSHEET_ID = '1y0pz5SzXEUc4PvjJy_hvA48g36e0usQjLvp9BQxHJxs'

# The ID for our specific device - used for if we have multiple devices 
DEVICE_ID = 0


def update_sheet(sheetname="Sheet1", link="0", title="0", channel="0"):  
    """update_sheet method:
       appends a row of a sheet in the spreadsheet with the 
       the link, title, and channel information 
    """
    # authentication, authorization step
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    creds = ServiceAccountCredentials.from_json_keyfile_name( 
            'hack-the-bottle.json', SCOPES)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API, append the next row of sensor data
    # values is the array of rows we are updating, its a single row
    # Format: Datetime	Device ID	Video Link	Video Name	Channel Name
    values = [ [ str(datetime.datetime.now()), DEVICE_ID,
                 link, title, channel ] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
                spreadsheetId=MY_SPREADSHEET_ID, 
                range=sheetname + '!A2:E2', 
                valueInputOption='USER_ENTERED', 
                insertDataOption='INSERT_ROWS',
                body=body).execute()                     


def main():  
    """main method:
       call update_sheets method to link information to the spreadsheet
    """
    link = "https://www.youtube.com/watch?v=VD6xJq8NguY"
    title = "There Is Something Hiding Inside Earth"
    channel = "Kurzgesagt - In a Nutshell"

    print ('Link: ', link)
    print ('Title: ', title)
    print ('Channel: ', channel)
    update_sheet("Sheet1", link, title, channel)


if __name__ == '__main__':  
    main()
