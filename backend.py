from hashlib import blake2b
import os
import string
import json
import random


def hashify(data):
    hashified = blake2b(data.encode(), digest_size=15).hexdigest()
    return hashified


def load_user_db(username):
    try:
        with open(f"users/{hashify(username)}.json", "r") as infile:
            user_data_dict = json.loads(infile.read())
            return user_data_dict
    except Exception as e:
        print(f"Could not load user, error: {e}")


def save_user(username, data):
    if not os.path.exists("users"):
        os.mkdir("users")
    try:
        with open(f"users/{hashify(username)}.json", "w") as outfile:
            outfile.write(json.dumps(data))
            return True
    except Exception as e:
        print(f"Could not create user, error: {e}")
        return False


def hash_password(password):
    salt = "bismuth"
    passhash = blake2b(digest_size=30)
    passhash.update((password + salt).encode())
    return passhash.hexdigest()


def add_user(user, password):
    user_data = {user: {"password": hash_password(password)}}
    save_user(user, user_data)


def exists_user(user):
    if os.path.exists(f"users/{user}.json"):
        return True
    else:
        return False


def login_validate(user, password):
    user_data = load_user_db(user)
    if user_data[user]["password"] == hash_password(password):
        return True
    else:
        return False


def cookie_get():
    filename = "cookie_secret"
    if not os.path.exists(filename):
        cookie_secret = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        with open(filename, "w") as infile:
            infile.write(cookie_secret)
    else:
        with open(filename) as infile:
            cookie_secret = infile.read()
    return cookie_secret
