import requests
import os
import json

# 2024年1月28日、なぜかこれだけUnauthorizedで取得できない

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# dev
# bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAAAenrwEAAAAAz%2Fj8aUNf%2FVXwYJWbKbGzi3UyWlY%3D8f1i4rTemX6vAcutguS14QybbUUiMUu5G6z9D3tXmoyF8X3NcG")
# standalone
bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAAG96sAEAAAAAl0nyqJgn6KgA6eZClGGvdyAxdBw%3Dg5QeOsLI0It8A2bjuMqtQqeloJohRA2mpszi3lm0ePloLKhRIm")

def create_url():
    # Replace with user ID below
    user_id = 2244994945
    return "https://api.twitter.com/2/users/{}/following".format(user_id)


def get_params():
    return {"user.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()