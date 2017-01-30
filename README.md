# Flamingo Challenge
This project aims at finding the **top 100 influencers** from social media (Youtube and Twitter) using API search.
[**Technical Challenge Answer.pdf**](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/Technical%20Challenge%20Answer.pdf) is the answer sheet for the challenge.

### API search:
Twitter and YouTube has their own tutorials for developers on API search. However, it is noticeable that they all pose certain **rate limit** for developers.

YouTube: 
> (Overview) https://developers.google.com/youtube/

> (Python Code Samples) https://developers.google.com/youtube/v3/code_samples/python#search_by_keyword

Twitter: 
> (Overview) https://dev.twitter.com/overview/api

> (API format) https://dev.twitter.com/overview/api/users (users) https://dev.twitter.com/overview/api/tweets (tweets)

> (Search API) https://dev.twitter.com/rest/reference/get/search/tweets

It comprises of two separate files for YouTube and Twitter search respectively.

## YouTube:

[**YouTube_script.py**](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/YouTube/Youtube_script.py) is the one-in-all script that request for API search, parse data and do simple sorting for SubscriberCount
and output analytics in dataframe ['ChannelTitle', 'ChannelID', 'SubscriberCount'], which can be referred in [**output_youtube.csv**](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/YouTube/output_youtube.csv).

## Twitter

Twitter files is a bit more complicated.

[**Twitter_one_keyword**](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/Twitter/Twitter_one_keyword.py) uses API keyword search and parse all relevant fields into one dataframe for each keyword. There is a sleep command at last to prevent hitting the rate limit.

Revelant 11 fields includes:

tweet_favorite | tweet_id	 | tweet_retweet | user_favorite |	user_follower	| user_friend | user_mention_id	| user_mention_screen_name |	user_mention_statuses	| user_screen_name	| user_statuses
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Though the project only utilized part of the stats for its ranking.

**Twitter_one_keyword** will output 26 different csv. files for each keyword, [**data_twitter_Minecraft.csv**](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/Twitter/data_twitter_Minecraft.csv) is included as a demo.
<br/>
<br/>
***
Moving to second part, [**Twitter_two_postprocess.py**](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/Twitter/Twitter_two_postprocess.py) does the necessary post-crawling analysis, and generate **4 different metrics** namely

all_sorted_follower_user |all_sorted_follower_user_mention | all_user_retweet_count | all_user_mention_count
--- | --- | --- | --- 

and **2 plot** showing the scattered plot for [favorite vs. retweet](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/Twitter/figure_1_retweet_vs_fav.png) and [user_mentioned vs. retweet](https://github.com/yang0339/Python3-FlamingoChallenge-Twitter-Youtube-API/blob/master/Twitter/figure_2_user_mentioned_vs_retweet.png), indicating there exists no hidden relations between them and that all metrics could only tell part of the story.

