import tweepy
import pprint as p
import json
import pandas as pd
import time

auth = tweepy.OAuthHandler('u1RlRjJ8RFu258PaUEAkVm847','peqJF5uYSyx9sAHwrqFAmEo5ZpZM8txck2b6wYLBmmPxK8HBPr')
auth.set_access_token('748473158974349312-686AdyONcoo8tdoDyrOd1T0m6jw606f','XvahDmqIXNrzE6OWxVeEHM8aMrzNgXRwFlL6DvsYH7LwV')

api = tweepy.API(auth)

def TWEET_SEARCH(previous_id,keyword):
    # initialization: parameters of interest: user (6) + user_mention (6) + tweet (3) = 15
    tweet_id = []
    tweet_favorite = []
    tweet_retweet = []

    user_id = []
    user_screen_name = []
    user_favorite = []
    user_follower = []
    user_friend = []
    user_statuses = []

    user_mention_id = []
    user_mention_screen_name = []
    user_mention_favorite = []
    user_mention_follower = []
    user_mention_friend = []
    user_mention_statuses = []

    print(previous_id)
    public_tweets = api.search(q=keyword, result_type='', since_id=previous_id, count=50)
    # print(public_tweets)
    # print(type(public_tweets)) # for check


    for tweet in public_tweets:
        tweet_json = json.loads(json.dumps(tweet._json))  # convert tp json format
        # print(type(tweet_json))
        # p.pprint(tweet_json) # for check

        user_mentions_info = tweet_json['entities']['user_mentions']
        if user_mentions_info != []:
            user_mention_id.append(user_mentions_info[0]['id_str'])
            user_mention_screen_name.append(user_mentions_info[0]['screen_name'])
        else:
            user_mention_id.append('N/A')
            user_mention_screen_name.append('N/A')
        user_id.append(tweet_json['user']['id_str'])
        user_screen_name.append(tweet_json['user']['screen_name'])
        user_favorite.append(str(tweet_json['user']['favourites_count']))
        user_follower.append(str(tweet_json['user']['followers_count']))
        user_friend.append(str(tweet_json['user']['friends_count']))
        user_statuses.append(str(tweet_json['user']['statuses_count']))

        tweet_id.append(tweet_json['id_str'])
        tweet_favorite.append(str(tweet_json['favorite_count']))
        tweet_retweet.append(str(tweet_json['retweet_count']))

    # extract user_mentions follower
    for entry in user_mention_id:
        try:
            public_user = api.get_user(user_id=entry)
            # print(type(public_user))
            user_json = json.loads(json.dumps(public_user._json))  # convert tp json format
            # p.pprint(user_json)

            user_mention_favorite.append(str(user_json['favourites_count']))
            user_mention_follower.append(str(user_json['followers_count']))
            user_mention_friend.append(str(user_json['friends_count']))
            user_mention_statuses.append(str(user_json['statuses_count']))

        except tweepy.error.TweepError as err:
            user_mention_favorite.append('N/A')
            user_mention_follower.append('N/A')
            user_mention_friend.append('N/A')
            user_mention_statuses.append('N/A')

    database_df = pd.DataFrame({'tweet_id': tweet_id \
                                   , 'tweet_favorite': tweet_favorite \
                                   , 'tweet_retweet': tweet_retweet \
                                   , 'user_id': user_id \
                                   , 'user_screen_name': user_screen_name \
                                   , 'user_favorite': user_favorite \
                                   , 'user_follower': user_follower \
                                   , 'user_friend': user_friend \
                                   , 'user_statuses': user_statuses \
                                   , 'user_mention_id': user_mention_id \
                                   , 'user_mention_screen_name': user_mention_screen_name \
                                   , 'user_mention_favorite': user_mention_favorite \
                                   , 'user_mention_follower': user_mention_follower \
                                   , 'user_mention_friend': user_mention_friend \
                                   , 'user_mention_statuses': user_mention_statuses})
    # print(database_df) # for check
    return database_df

def Build_Data(name):
    # conver the raw data to Pandas to write into csv file
    temp_df = pd.DataFrame()
    final_df = pd.DataFrame()
    for num in range(0, 20):
        if num == 0:
            since_id = 0
        else:
            # alternatively can call TWEET_SEARCh for max_id,
            # in that case change the var 'since_id' to int(temp_df['tweet_id'].max())+1
            since_id = int(temp_df['tweet_id'].min())-1
        temp_df = TWEET_SEARCH(since_id, name)
        final_df = pd.concat([final_df, temp_df], ignore_index=True)

    final_df.to_csv('data_twitter_%s.csv'% name,  sep=',', encoding='utf-8')


if __name__ == "__main__":
    for num in range(0, 26): # in total 26 items
        if num == 0:
            keyword = 'Gaming'
        if num == 1:
            keyword = 'Minecraft'
        if num == 2:
            keyword = 'Overwatch'
        if num == 3:
            keyword = 'World of warcraft'
        if num == 4:
            keyword = 'Counter Strike'
        if num == 5:
            keyword = 'Diablo'
        if num == 6:
            keyword = 'StarCraft'
        if num == 7:
            keyword = 'Grand Theft Auto'
        if num == 8:
            keyword = 'Gran Turismo'
        if num == 9:
            keyword = 'The Last of Us'
        if num == 10:
            keyword = 'Uncharted'
        if num == 11:
            keyword = 'Final Fantasy'
        if num == 12:
            keyword = 'Call of Duty'
        if num == 13:
            keyword = 'FIFA'
        if num == 14:
            keyword = '2K16'
        if num == 15:
            keyword = 'Destiny'
        if num == 16:
            keyword = 'Battlefield'
        if num == 17:
            keyword = 'Nintendo Land'
        if num == 18:
            keyword = 'Hyrule Warriors'
        if num == 19:
            keyword = 'Pokken Tournament'
        if num == 20:
            keyword = 'Dota2'
        if num == 21:
            keyword = 'Team Fortress'
        if num == 22:
            keyword = 'Unturned'
        if num == 23:
            keyword = 'Pokemon Go '
        if num == 24:
            keyword = 'Clash of Clans '
        if num == 25:
            keyword = 'Candy  Crush'
        print(num)

        Build_Data(keyword)

        # prevent the overflow of rate limit
        time.sleep(600)

