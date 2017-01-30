#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib.request as url
import json
import pprint as p
import pandas as pd

# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBydabOXFlELtLRk0sgSWa5k_SM2a5_iSg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results,
    # here to add other parameters
    order=options.order,
    pageToken=options.pageToken,
    type=options.type
  ).execute()

  channels = []
  CH_ID = []

  # Add each result to the appropriate list, and then display the lists of matching channels.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
      CH_ID.append('%s' % search_result["id"]["channelId"])

  # print ("Channels:\n", "\n".join(channels), "\n")
  # print(CH_ID) # for check
  return CH_ID


if __name__ == "__main__":
    Channel_id = []

    # here to add
    number_of_result = 25
    order = 'viewCount'
    pageToken = ''  # leave blank and will update when first query is sent
    type = 'channel'

    for num in range(0,26): # in total 26 items
        if num == 0:
            keyword = 'Gaming'
        if num == 1:
            keyword = 'Minecraft'
        if num == 2:
            keyword = 'Overwatch'
        if num == 3:
             keyword = 'WOW | World of War'
        if num == 4:
             keyword = 'CS|counter-strike|counter strike'
        if num == 5:
             keyword = 'Diablo'
        if num == 6:
             keyword = 'StarCraft'
        if num == 7:
            keyword = 'Grand Theft Auto'
        if num == 8:
            keyword ='Gran Turismo'
        if num == 9:
            keyword ='The Last of Us'
        if num == 10:
            keyword ='Uncharted'
        if num == 11:
            keyword = 'Final Fantasy'
        if num == 12:
            keyword = 'Call of Duty'
        if num == 13:
            keyword = 'FIFA'
        if num == 14:
            keyword = '2K16'
        if num == 15:
            keyword ='Destiny'
        if num == 16:
            keyword ='Battlefield'
        if num == 17:
            keyword = 'Nintendo Land'
        if num == 18:
            keyword ='Hyrule Warriors'
        if num == 19:
            keyword ='Pokken Tournament'
        if num == 20:
            keyword = 'Dota 2|Data2'
        if num == 21:
            keyword ='Team Fortress'
        if num == 22:
            keyword ='Unturned'
        if num == 23:
            keyword = 'Pokemon Go '
        if num == 24:
            keyword ='Clash of Clans '
        if num == 25:
            keyword ='Candy Crush'

        argparser.add_argument("--q", help="Search term", default=keyword)
        argparser.add_argument("--max_results", help="Max results", default=number_of_result)

         # here to add other parameters
        argparser.add_argument('--order', help='date, rating, relevance, title, videoCount, viewCount',
        default=order)
        argparser.add_argument('--pageToken', help='The pageToken parameter identifies a specific page'
         'in the result set that should be returned. In an API response, the nextPageToken and prevPageToken'
         'properties identify other pages that could be retrieved.',
        default = pageToken)
        argparser.add_argument('--type', help='channel, playlist, video', default=type)

        args = argparser.parse_args()
        # print('args = ', args)
        # print('num = ', num) # for check
        try:
            CH_ID = youtube_search(args)
            Channel_id.append(CH_ID)
            argparser.__init__() # intialize the parser to accept new round of API query
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    # dimension of the nested list: 26 * 25: 26 games. every game top 25 channels
    # use the channel_id to find the number of subscribers
    # sample request: https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC-lHJZR3Gqxm24_Vd_AJ5Yw&key=AIzaSyBydabOXFlELtLRk0sgSWa5k_SM2a5_iSg

    subscriber = []
    for count1 in range(0,len(Channel_id)):
        for count2 in range(0,len(Channel_id[count1])):
            # construct url for API Channel query
            channel_url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id='
            channel_url += (str(Channel_id[count1][count2]))
            channel_url += '&key=AIzaSyBydabOXFlELtLRk0sgSWa5k_SM2a5_iSg' # developer API key
            with url.urlopen(channel_url) as response:
                info = json.loads(response.read().decode('utf-8'))
                temp = info['items']
                subscriber.append([int(temp[0]['statistics']['subscriberCount']), (temp[0]['id'])])
    # p.pprint(subscriber) # for check

    # transform to dataframe for post-processing
    df = pd.DataFrame(subscriber, columns=['subscriberCount', 'ChannelID'])
    df = df.sort_values('subscriberCount', ascending=False)
    # check duplicate, if page_token not correctly functioning, df would be absurdly small
    df = df.drop_duplicates(subset='ChannelID', keep='first')
    # print(df) # for check

    Top_100 = df[:100].values.tolist()
    # print(Top_100)
    output = []
    # example query for search: https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&channelId=UCVtFOytbRpEvzLjvqGG5gxQ&key={YOUR_API_KEY}
    for count in range(0,100):
        channel_url = 'https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&channelId='
        channel_url += Top_100[count][1]
        channel_url += '&key=AIzaSyBydabOXFlELtLRk0sgSWa5k_SM2a5_iSg'
        with url.urlopen(channel_url) as response:
            info = json.loads(response.read().decode('utf-8'))
            temp = info['items']
            # print(temp[0]['snippet']['channelTitle'])
            output.append([temp[0]["snippet"]["channelTitle"], Top_100[count][1], Top_100[count][0]])

    # transform to dataframe for file writing
    output_df = pd.DataFrame(output, columns=['ChannelTitle', 'ChannelID', 'SubscriberCount'])
    # output_df.to_csv('output_youtube.csv', sep=',', encoding='utf-8')
    # target = codecs.open('output_youtube.csv', 'w', 'utf-8')
    print(output_df)