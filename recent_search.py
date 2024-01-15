# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

import requests
import os
import json

API_KEY = "OGHUuZIAaswYX3YMXbNOv1bHV"
API_SECRET = "0rw4WWImwkgs7itLD4LyqECLD2OfuZkZ3VAABPgR14hK3BZJ5T"
ACCESS_TOKEN = "1229650988216115200-CntDVVABeE7sF5SPinnEhHmyGoSV6Q"
ACCESS_TOKEN_SECRET = "4vTSdq2gjMgMEQvrBdirNIXwO4G8tmyMWBVngNsFphFkT"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAAenrwEAAAAAz%2Fj8aUNf%2FVXwYJWbKbGzi3UyWlY%3D8f1i4rTemX6vAcutguS14QybbUUiMUu5G6z9D3tXmoyF8X3NcG"

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get(BEARER_TOKEN)

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()

# result
# 200
# {
#     "data": [
#         {
#             "author_id": "1745401123979067392",
#             "edit_history_tweet_ids": [
#                 "1746719547187405158"
#             ],
#             "id": "1746719547187405158",
#             "text": "custom share text https://t.co/w892Io9wPL #twitterdev via @example,demo"
#         },
#         {
#             "author_id": "4242850460",
#             "edit_history_tweet_ids": [
#                 "1745547266050716156"
#             ],
#             "id": "1745547266050716156",
#             "text": "RT @AuctionBio: Wanna dominate tech world in 2024? My video unveils TOP 5 programming languages u NEED to learn\nDiscover trending tech, AI,\u2026"
#         },
#         {
#             "author_id": "19622890",
#             "edit_history_tweet_ids": [
#                 "1745462870207561778"
#             ],
#             "id": "1745462870207561778",
#             "text": "@__mharrison__ Are you telling me that my avatar of a famous Colombian clown is not serious enough for #TwitterDev ?"
#         },
#         {
#             "author_id": "916683518",
#             "edit_history_tweet_ids": [
#                 "1745043289894728038"
#             ],
#             "id": "1745043289894728038",
#             "text": "Calling all #TwitterDev &amp; #Tester @testingclub  @ministryoftest  @testingmag @googletesting ! Stay up-to-date on the latest software testing news &amp; insights with my blog! Follow me https://t.co/fA7ptZbymC for fresh content &amp; connect with the testing community!"
#         },
#         {
#             "author_id": "1642542657942454272",
#             "edit_history_tweet_ids": [
#                 "1744939542090596609"
#             ],
#             "id": "1744939542090596609",
#             "text": "@AvivaKlompas @ICRC I'm creating a silhouette logo. If you have any files now, I can design them for you. I am available on Fiverr. https://t.co/m4VH6sc5Yh\n#twitterdata #twitterdev #twitterdublin #twitterdummy #twitterele #twitterengagement #twitterer #twitterers #TwitterChange #twittercat #TwitterX https://t.co/FaOIhN8XzS"
#         },
#         {
#             "author_id": "1642542657942454272",
#             "edit_history_tweet_ids": [
#                 "1744939473249398794"
#             ],
#             "id": "1744939473249398794",
#             "text": "@TheFigen_ I'm creating a silhouette logo. If you have any files now, I can design them for you. I am available on Fiverr. https://t.co/m4VH6sc5Yh\n#twitterdata #twitterdev #twitterdublin #twitterdummy #twitterele #twitterengagement #twitterer #twitterers #TwitterChange #twittercat #TwitterX https://t.co/cn07rTUjR7"
#         },
#         {
#             "author_id": "1642542657942454272",
#             "edit_history_tweet_ids": [
#                 "1744939423282733158"
#             ],
#             "id": "1744939423282733158",
#             "text": "@JoeBiden I'm creating a silhouette logo. If you have any files now, I can design them for you. I am available on Fiverr. https://t.co/m4VH6sc5Yh\n#twitterdata #twitterdev #twitterdublin #twitterdummy #twitterele #twitterengagement #twitterer #twitterers #TwitterChange #twittercat #TwitterX https://t.co/cszJVbumsC"
#         },
#         {
#             "author_id": "1642542657942454272",
#             "edit_history_tweet_ids": [
#                 "1744939372435185925"
#             ],
#             "id": "1744939372435185925",
#             "text": "@CollinRugg I'm creating a silhouette logo. If you have any files now, I can design them for you. I am available on Fiverr. https://t.co/m4VH6sc5Yh\n#twitterdata #twitterdev #twitterdublin #twitterdummy #twitterele #twitterengagement #twitterer #twitterers #TwitterChange #twittercat #TwitterX https://t.co/KSlFqjmeFp"
#         },
#         {
#             "author_id": "1642542657942454272",
#             "edit_history_tweet_ids": [
#                 "1744939318458618185"
#             ],
#             "id": "1744939318458618185",
#             "text": "@IDF I'm creating a silhouette logo. If you have any files now, I can design them for you. I am available on Fiverr. https://t.co/m4VH6sc5Yh\n#twitterdata #twitterdev #twitterdublin #twitterdummy #twitterele #twitterengagement #twitterer #twitterers #TwitterChange #twittercat #TwitterX https://t.co/BpLrKUUeGx"
#         },
#         {
#             "author_id": "1642542657942454272",
#             "edit_history_tweet_ids": [
#                 "1744939243581878379"
#             ],
#             "id": "1744939243581878379",
#             "text": "@iamyesyouareno I'm creating a silhouette logo. If you have any files now, I can design them for you. I am available on Fiverr. https://t.co/m4VH6sc5Yh\n#twitterdata #twitterdev #twitterdublin #twitterdummy #twitterele #twitterengagement #twitterer #twitterers #TwitterChange #twittercat #TwitterX https://t.co/VAeYPWnZhF"
#         }
#     ],
#     "meta": {
#         "newest_id": "1746719547187405158",
#         "next_token": "b26v89c19zqg8o3fr5neox10mca3ngupjko1lhqyzdf99",
#         "oldest_id": "1744939243581878379",
#         "result_count": 10
#     }
# }
