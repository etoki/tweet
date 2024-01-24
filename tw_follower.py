import tweepy
from pprint import pprint

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


# ★ユーザーIDを指定
user_id = '1229650988216115200' # etokiwa999

# 関数
def GetUser_Follower(user_id):
    # メソッド
    following = ClientInfo().get_users_followers(id=int(user_id))
    # following = ClientInfo().get_users_followers(id=int(user_id), max_results=10)
    
    # 取得したデータ加工
    results     = []
    follow_data = following.data

    # tweet検索結果取得
    if follow_data != None:
        for tweet in follow_data:
            obj = {}
            obj["user_id"]  = tweet.id       # User_ID
            obj["name"]     = tweet.name     # Name
            obj["username"] = tweet.username #username
            results.append(obj)
    else:
        results.append('')

    # 結果出力
    return results

pprint(GetUser_Follower(user_id))