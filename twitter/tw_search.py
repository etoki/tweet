import tweepy
from pprint import pprint
import pandas as pd

# API情報を記入
BEARER_TOKEN        = "AAAAAAAAAAAAAAAAAAAAAAenrwEAAAAAz%2Fj8aUNf%2FVXwYJWbKbGzi3UyWlY%3D8f1i4rTemX6vAcutguS14QybbUUiMUu5G6z9D3tXmoyF8X3NcG"
API_KEY             = "OGHUuZIAaswYX3YMXbNOv1bHV"
API_SECRET          = "0rw4WWImwkgs7itLD4LyqECLD2OfuZkZ3VAABPgR14hK3BZJ5T"
ACCESS_TOKEN        = "1229650988216115200-CntDVVABeE7sF5SPinnEhHmyGoSV6Q"
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
search     = "ギフテッド -増田 -浮所 -ジャニーズ -ドラマ -NEWS -美少年 -アーティスト -ミステリ -ダンス -白饅頭 -is:quote -is:retweet"  # 検索対象
tweet_max  = 10  # 取得したいツイート数(10〜100で設定可能)
start_time = "2024-01-24T00:00:00Z"
end_time   = "2024-01-25T23:59:59Z"

# 関数
def SearchTweets(search,tweet_max,start_time,end_time):    
    # 直近のツイート取得
    tweets = ClientInfo().search_recent_tweets(
                                                query = search, 
                                                max_results = tweet_max,
                                                tweet_fields=["created_at","public_metrics"],
                                                # user_fields=["description","public_metrics"],
                                                expansions = ['author_id'],
                                                start_time = start_time,
                                                end_time   = end_time)

    # 取得したデータ加工
    result = []

    # tweet検索結果取得
    if tweets.data != None:
        for tweet in tweets.data:
            obj = {}
            obj["tweet_id"] = tweet.id
            obj["text"] = tweet.text
            # obj["tw_public_metrics"] = tweet.public_metrics
            obj["created_at"] = tweet.created_at
            obj["author_id"] = tweet.author_id
            obj.update(tweet.public_metrics)
            result.append(obj)
    else:
        result.append('')
        print("検索ワードに該当するツイートがありません。")
    return result

# 関数実行・出力
df = SearchTweets(search,tweet_max,start_time,end_time)
df = pd.DataFrame(df)
df.to_csv('output.csv', index=False) 
pprint(df)

