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

# ★ツイートIDを指定
tweet_id = '1747437199245910436'
# https://twitter.com/odasaburo99/status/1747437199245910436

# ファボ（いいね）のユーザーリスト取得
def Get_Liking_Users(tweet_id):
    # メソッド実行
    users = ClientInfo().get_liking_users(id=int(tweet_id)).data
    
    # 結果加工
    results = []
    if users !=  None:
        for i in range(len(users)):
            obj = {}
            obj["user_id"]  = users[i].id
            obj["name"]     = users[i].name
            obj["username"] = users[i].username
            results.append(obj)
    else:
        results.append("")
    
    df = pd.DataFrame(results)

    # 出力
    return df

# リツイートのユーザーリスト取得
def Get_Retweeters(tweet_id):
    # メソッド実行
    users = ClientInfo().get_retweeters(id=int(tweet_id)).data
    
    # 結果加工
    results = []
    if users != None:
        for i in range(len(users)):
            obj = {}
            obj["user_id"]  = users[i].id
            obj["name"]     = users[i].name
            obj["username"] = users[i].username
            results.append(obj)
    else:
        results.append("")
    
    df = pd.DataFrame(results)
    
    # 出力
    return df

# 関数実行・結果出力

# ファボ（いいね）のユーザーリスト取得
# pprint(Get_Liking_Users(tweet_id))

# リツイートのユーザーリスト取得
pprint(Get_Retweeters(tweet_id))
