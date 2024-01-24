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


# ★ツイートIDを指定
tweet_id = '1747437199245910436'
# https://twitter.com/odasaburo99/status/1747437199245910436


# 関数
def GetTweet(tweet_id):
    # メソッド実行
    GetTwt = ClientInfo().get_tweet(id=int(tweet_id), expansions=["author_id"], user_fields=["username"])

    # 結果加工
    twt_result = {}
    twt_result["tweet_id"] = tweet_id
    twt_result["user_id"]  = GetTwt.includes["users"][0].id
    twt_result["username"] = GetTwt.includes["users"][0].username
    twt_result["text"]     = GetTwt.data
    twt_result["url"]      = "https://twitter.com/" + GetTwt.includes["users"][0].username + "/status/" + str(tweet_id)

    # 結果出力
    return twt_result

# 関数実行・出力
pprint(GetTweet(tweet_id))