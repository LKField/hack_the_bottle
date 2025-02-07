import pandas as pd
from publish2GSheet import update_sheet, get_values

data_strct = {'Date Time': {},
              'Device ID': {},
              'Video Link': {},
              'Video Name': {},
              'Channel Name': {}}
df = pd.DataFrame(data_strct)

for i in range(2,20):
    data_range = '!A' + str(i) + ':' + 'E' + str(i)
    video_data = get_values(sheetname="Sheet1", range=data_range) 

    """     date_time = video_data[0][0]
    device_id = video_data[0][1]
    link = video_data[0][2]
    title = video_data[0][3]
    channel = video_data[0][4] """

    new_row = pd.DataFrame({'Date Time': video_data[0][0], 
                            'Device ID': video_data[0][1], 
                            'Video Link': video_data[0][2],
                            'Video Name': video_data[0][3],
                            'Channel Name': video_data[0][4]},
                            index =[0])

    df = pd.concat([new_row, df]).reset_index(drop = True)

print("DataFrame", df)
