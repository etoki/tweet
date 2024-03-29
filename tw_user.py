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

# ★ユーザーIDを指定
user_id = '1229650988216115200'  # etokiwa999

# 関数
def GetUser(user_id):
    # メソッド
    GetUser = ClientInfo().get_user(id=int(user_id), 
                                    user_fields=[
                                        "created_at",
                                        "description",
                                        "location",
                                        "protected",
                                        "public_metrics"]).data
    
    # pprint(type(GetUser))
    # test = GetUser
    # pprint(test.keys())
    # pprint(test.description)

    # 結果加工
    result  = {
        "user_id": user_id,
        "name": GetUser.name,
        "username": GetUser.username,
        "created_at": GetUser.created_at,
        "location": GetUser.location,
        "protected": GetUser.protected,
        "description": GetUser.description
        # "public_metrics": GetUser.public_metrics
    }
    result.update(GetUser.public_metrics)
    # result = pd.Series(result)

    # 結果出力
    return result

# 関数実行・結果出力
pprint(GetUser(user_id))

# 複数のユーザーをdataframeに入れる
# results = []
# results.append(GetUser(user_id))
# results.append(GetUser(user_id))
# results.append(GetUser(user_id))
# results = pd.DataFrame(results)
# pprint(results)
