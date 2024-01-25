import tweepy
from pprint import pprint
import pandas as pd

# API情報を記入
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAenrwEAAAAAz%2Fj8aUNf%2FVXwYJWbKbGzi3UyWlY%3D8f1i4rTemX6vAcutguS14QybbUUiMUu5G6z9D3tXmoyF8X3NcG"
API_KEY = "OGHUuZIAaswYX3YMXbNOv1bHV"
API_SECRET = "0rw4WWImwkgs7itLD4LyqECLD2OfuZkZ3VAABPgR14hK3BZJ5T"
ACCESS_TOKEN = "1229650988216115200-CntDVVABeE7sF5SPinnEhHmyGoSV6Q"
ACCESS_TOKEN_SECRET = "4vTSdq2gjMgMEQvrBdirNIXwO4G8tmyMWBVngNsFphFkT"


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    
    return client

# ★必要情報入力
search    = "ギフテッド"  # 検索対象
tweet_max = 10           # 取得したいツイート数(10〜100で設定可能)

# 関数
def SearchTweets(search,tweet_max):    
    # 直近のツイート取得
    tweets = ClientInfo().search_recent_tweets(
                                                query = search, 
                                                max_results = tweet_max,
                                                tweet_fields=["public_metrics"],
                                                # user_fields=["description","public_metrics"],
                                                expansions = ['author_id'])

    # 取得したデータ加工
    results     = []

    # tweet検索結果取得
    if tweets.data != None:
        for tweet in tweets.data:
            obj = {}
            obj["tweet_id"] = tweet.id
            obj["text"] = tweet.text
            # obj["tw_public_metrics"] = tweet.public_metrics
            obj["author_id"] = tweet.author_id
            obj.update(tweet.public_metrics)
            # for i in range(len(tweets.includes['users'])):
            #     if tweet.author_id == tweets.includes['users'][i]['id']:
            #         obj['user'] = tweets.includes['users'][i]['name']
            #         obj['username'] = tweets.includes['users'][i]['username']
            #         obj['description'] = tweets.includes['users'][i]['description']
            #         obj['user_public_metrics'] = tweets.includes['users'][i]['public_metrics']
            #         obj.update(tweets.includes['users'][i]['public_metrics'])

            results.append(obj)
    else:
        results.append('')
        print("検索ワードに該当するツイートがありません。")

    df = pd.DataFrame(results)
    df.to_csv('output.csv', index=False) 

    # 結果出力
    return df

# 関数実行・出力
pprint(SearchTweets(search,tweet_max))
