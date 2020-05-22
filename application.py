from flask_restful import  Resource, Api
from flask import Flask, request,abort
import pandas as pd
import time, json
import datetime
import got3

day_date = datetime.date.today()
day_date = day_date.isoformat()

application  = Flask(__name__)
api = Api(application)



def Scrap(name,scrap_by='user', since='2019-01-10', till='2019-02-12', max=100, save=False):
    
    tweets_text = []
    tweets_ids  = []
    user_name   = []
    tweet_replies = []
    permalink = []
    favorites = []
    hashtags = []
    urls = []
    tweets_min  = []
    tweets_retweets = []
    tweets_time = []
    
    if scrap_by == 'user':

        tweetCriteria = got3.manager.TweetCriteria().setUsername(name).setSince(since).setUntil(till).setMaxTweets(max)
        tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
        for tweet in tweets:

            tweets_text.append(tweet.text)
            tweets_ids.append(tweet.id)
            favorites.append(tweet.favorites)
            tweet_replies.append(tweet.replies)
            hashtags.append(tweet.hashtags)
            urls.append(tweet.urls)
            tweets_min.append(int(tweet.date.minute))
            tweets_retweets.append(int(tweet.retweets))
            tweets_time.append(tweet.time)
            permalink.append(tweet.permalink)
        
        # print(len(tweets_text))
        df = pd.DataFrame()
        df['id'] = tweets_ids
        df['text'] = tweets_text
        df['favorites'] = favorites
        df['hashtags'] = hashtags
        df['replies'] = tweet_replies
        df['urls'] = urls
        df['permalinks'] = permalink
        df['retweets'] = tweets_retweets
        df['time_sec'] = tweets_time
        df['name'] = name
        if save:
            df.to_csv(name+'.csv', encoding='utf-8')
        
        return df
                
    elif scrap_by == 'word':
        tweetCriteria = got3.manager.TweetCriteria().setQuerySearch(name).setSince(since).setUntil(till).setMaxTweets(max)
        tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
        
        for tweet in tweets:

            tweets_text.append(tweet.text)
            user_name.append(tweet.username)
            tweets_ids.append(tweet.id)
            tweet_replies.append(tweet.replies)
            favorites.append(tweet.favorites)
            hashtags.append(tweet.hashtags)
            urls.append(tweet.urls)
            tweets_min.append(int(tweet.date.minute))
            tweets_retweets.append(int(tweet.retweets))
            tweets_time.append(tweet.time)
            permalink.append(tweet.permalink)


        df = pd.DataFrame()
        df['id'] = tweets_ids
        df['text'] = tweets_text
        df['user_name'] = user_name
        df['favorites'] = favorites
        df['replies'] = tweet_replies
        df['hashtags'] = hashtags
        df['urls'] = urls
        df['permalinks'] = permalink
        df['retweets'] = tweets_retweets
        df['time_sec'] = tweets_time
        df['name'] = name
        if save:
            df.to_csv(name+'.csv', encoding='utf-8')
            
        return df




class TweetScrape(Resource):
    def post(self):
        data = request.get_json(force=True)
        try:
            name, scrapeType, since, till, maxTweets = data['name'], data['scrapeType'], data['since'], data['till'], data['maxTweets']
        except:
            abort(404, 'Given parameters is wrong or not complete, please check it again, params is: {name, scrapeType,since,till},maxTweets')

        data = Scrap(name, scrapeType, since, till, int(maxTweets))
            # abort(404, 'There is no tweets for this name, or name is wrong, please double check name and data first')
        if len(data) == 0:
            abort(404, 'There is no enough tweets for this name, or the name is wrong, please double check name and data first')
        # dataJson = json.dumps(data, ensure_ascii=False)
        js = data.to_json(force_ascii =False,orient='records')
        return js



api.add_resource(TweetScrape, '/ScrapeTweets/')

if __name__ == "__main__":
    application.run(debug=False)


