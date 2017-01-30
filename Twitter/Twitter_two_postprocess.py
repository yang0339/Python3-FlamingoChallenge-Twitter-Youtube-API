import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sum_tweet = pd.DataFrame()
all_sorted_follower_user = pd.DataFrame()
all_sorted_follower_user_mention = pd.DataFrame()
all_user_retweet_count = pd.DataFrame()
all_user_mention_count = pd.DataFrame()


for num in range(0, 26):  # in total 26 items
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

    raw_data = pd.read_csv('data_twitter_%s.csv'% keyword,  sep=',', encoding='utf-8')
    # drop duplicate, just in case
    raw_data = raw_data.drop_duplicates(subset='tweet_id', keep='first')
    # print([raw_data['tweet_retweet'].sum(),raw_data['tweet_favorite'].sum()]) # for check

    # a var store the info only for tweet_retweet amd tweet_favorite for subsequent visualization
    sum_tweet = sum_tweet.append([(raw_data['tweet_retweet'].sum(), raw_data['tweet_favorite'].sum())], ignore_index=True)


    # Reduce size of the dataframe, only extract useful elements
    # tweet: tweet_id, tweet_retweet
    # user: user_screen_name, user_follower
    # user_mention: user_mention_screen_name, user_mention_follower
    useful_data = raw_data.loc[:, lambda df:['tweet_retweet', 'user_screen_name', 'user_follower',\
                            'user_mention_screen_name', 'user_mention_follower']]



    # METRIC 1 & 2: popularity measured for individual user is the number of follower:
    sorted_follower_user = useful_data.sort_values('user_follower', ascending=False)\
                             .drop_duplicates(subset='user_screen_name', keep='first') \
                            [['user_screen_name', 'user_follower']].reset_index(drop=True)
    # print(sorted_follower_user.head(10))

    sorted_follower_user_mention = useful_data.sort_values('user_mention_follower', ascending=False)\
                                    .drop_duplicates(subset='user_mention_screen_name', keep='first') \
                                    [['user_mention_screen_name', 'user_mention_follower']].reset_index(drop=True)
    # print(sorted_follower_user_mention.head(10))



    # METRIC 3 & 4 : the user count in tweet weighing on the popularity of that tweet:
    # fot each user and user_mention, count the retweet for that particular twitter
    #user_count = pd.DataFrame({useful_data['user_screen_name', 'tweet_retweet']})
    user_retweet_count = useful_data.loc[:, lambda df: ['tweet_retweet', 'user_screen_name']].groupby(['user_screen_name']).sum() \
                        .reset_index().sort_values('tweet_retweet', ascending=False).reset_index(drop=True)
    # print(user_retweet_count.head(10))

    # fot each user and user_mention, count the retweet for that particular twitter
    user_mention_count = pd.DataFrame({'user_mention_counts': useful_data.groupby(['user_mention_screen_name']).size()})\
                        .reset_index().sort_values('user_mention_counts', ascending=False).reset_index(drop=True)
    # print(user_mention_count.head(10))


    all_sorted_follower_user = pd.concat([all_sorted_follower_user, pd.concat([sorted_follower_user, pd.DataFrame([str(keyword)]*len(sorted_follower_user), columns=['Game_name'])], axis=1)], ignore_index=True)
    all_sorted_follower_user_mention = pd.concat([all_sorted_follower_user_mention, pd.concat([sorted_follower_user_mention, pd.DataFrame([str(keyword)]*len(sorted_follower_user_mention), columns=['Game_name'])], axis=1)], ignore_index=True)
    all_user_retweet_count = pd.concat([all_user_retweet_count, pd.concat([user_retweet_count, pd.DataFrame([str(keyword)]*len(user_retweet_count), columns=['Game_name'])], axis=1)], ignore_index=True)
    all_user_mention_count = pd.concat([all_user_mention_count, pd.concat([user_mention_count, pd.DataFrame([str(keyword)]*len(user_mention_count), columns=['Game_name'])], axis=1)], ignore_index=True)

#print(all_sorted_follower_user) # OK
# print(all_sorted_follower_user_mention) # OK
#print(all_user_retweet_count) # OK
#print(all_user_mention_count) # OK

# write to csv
#all_sorted_follower_user.to_csv('all_sorted_follower_user.csv',  sep=',', encoding='utf-8')
#all_sorted_follower_user_mention.to_csv('all_sorted_follower_user_mention.csv',  sep=',', encoding='utf-8')
#all_user_retweet_count.to_csv('all_user_retweet_count.csv',  sep=',', encoding='utf-8')
#all_user_mention_count.to_csv('all_user_mention_count.csv',  sep=',', encoding='utf-8')

# sort across games
most_popular_user = all_sorted_follower_user.sort_values('user_follower', ascending=False).reset_index(drop=True)
most_mentnioned_user = all_sorted_follower_user_mention.sort_values('user_mention_follower', ascending=False).reset_index(drop=True)
most_recognized_user = all_user_retweet_count.sort_values('tweet_retweet', ascending=False).reset_index(drop=True)
most_recognized_user_mentioned = all_user_mention_count.sort_values('user_mention_counts',ascending=False).reset_index(drop=True)

#print('most_popular_user_tweet: \n',most_popular_user.head(20),'\n')
#print('most_popular_user_mentioned: \n', most_mentnioned_user.head(20),'\n')
#print('most_recognized_user_tweet: \n', most_recognized_user.head(20),'\n')
#print('most_recognized_user_mentioned: \n', most_reliable_user.head(20),'\n')


most_popular_user = most_popular_user.rename(columns={'user_screen_name': 'screen_name'})
most_mentnioned_user = most_mentnioned_user.rename(columns={'user_mention_screen_name': 'screen_name', 'user_mention_follower' : 'user_follower'})
metric_one_two = pd.merge(most_popular_user,most_mentnioned_user, on=['screen_name','Game_name','user_follower'])
metric_one_two = metric_one_two.sort_values('user_follower', ascending=False).reset_index(drop=True)
# metric_one_two.to_csv('metric_one_two.csv',  sep=',', encoding='utf-8')
# print(metric_one_two.head(100))

most_recognized_user = most_recognized_user.rename(columns={'user_screen_name': 'screen_name'})
most_recognized_user_mentioned = most_recognized_user_mentioned.rename(columns={'user_mention_screen_name': 'screen_name'})
metric_three_four = pd.merge(most_recognized_user,most_recognized_user_mentioned, on=['screen_name','Game_name'])
product = pd.DataFrame(metric_three_four['tweet_retweet'] * metric_three_four['user_mention_counts'], columns=['product'])
metric_three_four = pd.concat([metric_three_four, product],axis=1)
metric_three_four = metric_three_four.sort_values('product', ascending=False).reset_index(drop=True)
# metric_three_four.to_csv('metric_three_four.csv',  sep=',', encoding='utf-8')
# print(metric_three_four.head(100))

# find how many entries are the same in two lists
metric_twitter = pd.merge(metric_one_two.head(1000),metric_three_four.head(1000), on=['screen_name','Game_name'])
print(metric_twitter[['screen_name', 'Game_name']])


#--------------------------------------------------#
# visualization
# understand the relationship between tweet_retweet and tweet_favorite
plt.figure(1)
y = np.array(sum_tweet[1])
x = np.array(sum_tweet[0])/1000
# print(len(sum_tweet))
A = np.vstack([x, np.ones(len(sum_tweet))]).T
m, err = np.linalg.lstsq(A, y)[0]

# alternative: m, b = np.polyfit(sum_tweet[0], sum_tweet[1], 1)
area = (x/y/9)**1/16  # 0 to 15 point radiuses
colors = np.random.rand(26);
plt.scatter(x,y, s=10000*area, c=colors, alpha=0.5, label='data point')
plt.plot(x, m*x+err, 'r-.', label='linear regression line')
plt.xlabel('number of retweet (in 1,000)')
plt.ylabel('number of favorite')
plt.title('retweet vs. favorite')
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.text(800, 570, 'y = %s*x' %m)
plt.text(800, 500, 'err = %s' %err)
plt.legend()
plt.show()



plt.figure(2)
y = np.array(metric_three_four['tweet_retweet'])
x = np.array(metric_three_four['user_mention_counts'])
area = (y/x/1000)**1/16  # 0 to 15 point radiuses
colors = np.random.rand(len(metric_three_four));
plt.scatter(x,y, s=100, c=colors, alpha=0.5, label='data point')
plt.xlabel('number of mentions')
plt.ylabel('number of retweet')
plt.title('mentions vs. retweet')
plt.xlim(xmin=0)
plt.ylim(ymin=0, ymax=600)
plt.legend()
plt.show()