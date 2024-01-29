import instaloader
import json
import os
from instaloader import Profile
from datetime import date
from dotenv import load_dotenv
from typing import Dict

UNFOLLOWED_FILE_PATH = "unfollowed_you.json"
PREVIOUS_FOLLOWERS_FILE_PATH = "previous_time_followers.json"
NOT_FOLLOWING_FILE_PATH = "not_following_you.json"


def file_exists(file_path):
    return os.path.exists(file_path)


def read_json_file(file_path):
    try:
        with open(file_path, "r") as infile:
            return json.load(infile)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return None


def load_environment_variables():
    load_dotenv('.env')
    required_variables = ["INSTAGRAM_USERNAME", "INSTAGRAM_PASSWORD"]
    try:
        for variable in required_variables:
            if not os.getenv(variable):
                raise ValueError(f"Error: {variable} environment variable is not set.")
        return os.getenv(required_variables[0]), os.getenv(required_variables[1])
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    load_dotenv('.env')
    username, password = load_environment_variables()

    L = instaloader.Instaloader()
    L.login(username, password)

    profile = Profile.from_username(L.context, username)

    data: Dict = {"date": date.today().isoformat(), "followers": []}

    old_followers = read_json_file(PREVIOUS_FOLLOWERS_FILE_PATH) if file_exists(PREVIOUS_FOLLOWERS_FILE_PATH) else {}

    for follower in profile.get_followers():
        data["followers"].append(str(follower.username))

    followers_json_object = json.dumps(data, indent=2)
    with open(PREVIOUS_FOLLOWERS_FILE_PATH, "w") as outfile:
        outfile.write(followers_json_object)

    if bool(old_followers):
        unfollows = read_json_file(UNFOLLOWED_FILE_PATH) if file_exists(UNFOLLOWED_FILE_PATH) else []
        unfollowed = []
        for old_fw in old_followers["followers"]:
            if old_fw not in data["followers"]:
                unfollowed.append(old_fw)

        for ufw in unfollowed:
            unfollows.append({"date": date.today().isoformat(), "username": ufw})

        unfollows.sort(key=lambda x: x['date'], reverse=True)
        unfollowed_json_object = json.dumps(unfollows, indent=2)

        with open(UNFOLLOWED_FILE_PATH, "w") as outfile:
            outfile.write(unfollowed_json_object)

    # follows_not_following = []
    # for follow in profile.get_followees():
    #     if follow.followers < 5000:
    #         if str(follow.username) not in data['followers']:
    #             follows_not_following.append(str(follow.username))
    #
    # not_following_json_object = json.dumps(follows_not_following, indent=2)
    #
    # with open(NOT_FOLLOWING_FILE_PATH, "w") as outfile:
    #     outfile.write(not_following_json_object)
