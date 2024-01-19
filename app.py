import instaloader
import json
import os
from instaloader import Profile
from datetime import date
from dotenv import load_dotenv

UNFOLLOWED_FILE_PATH = "unfollowed_you.json"
PREVIOUS_FOLLOWERS_FILE_PATH = "previous_time_followers.json"


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


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


if __name__ == "__main__":
    load_dotenv('.env')
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    L = instaloader.Instaloader()
    L.login(username, password)

    profile = Profile.from_username(L.context, username)

    data = {"date": date.today().isoformat(), "followers": []}

    old_followers = {} if is_file_empty(PREVIOUS_FOLLOWERS_FILE_PATH) else read_json_file(PREVIOUS_FOLLOWERS_FILE_PATH)

    for follower in profile.get_followers():
        data["followers"].append(str(follower.username))

    followers_json_object = json.dumps(data, indent=2)
    with open(PREVIOUS_FOLLOWERS_FILE_PATH, "w") as outfile:
        outfile.write(followers_json_object)

    if bool(old_followers):
        unfollows = [] if is_file_empty(UNFOLLOWED_FILE_PATH) else read_json_file(UNFOLLOWED_FILE_PATH)
        differences = list(set(data['followers']) - set(old_followers["followers"]))
        unfollowed = list(set(differences) - set(old_followers["followers"]))

        for ufw in unfollowed:
            unfollows.append({"date": date.today().isoformat(), "username": ufw})

        unfollows.sort(key=lambda x: x['date'], reverse=True)
        unfollowed_json_object = json.dumps(unfollows, indent=2)

        with open(UNFOLLOWED_FILE_PATH, "w") as outfile:
            outfile.write(unfollowed_json_object)
