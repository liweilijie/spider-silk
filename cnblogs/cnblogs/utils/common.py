import hashlib
import pickle
import os


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()

def save_cookies(cookies_dict):
    ck_pkl = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ck.pkl")
    print(ck_pkl)
    print(cookies_dict)
    with open(ck_pkl, 'wb') as f:
        pickle.dump(cookies_dict, f)

def load_cookies():
    ck_pkl = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ck.pkl")
    cookies_dict = {}
    try:
        with open(ck_pkl, 'rb') as f:
            cookies_dict = pickle.load(f)
    except FileNotFoundError:
        return cookies_dict
    print(cookies_dict)
    return cookies_dict

if __name__ == "__main__":
    print(get_md5("https://cnblogs.com"))
    cookies_dict = {"hello": "python"}
    save_cookies(cookies_dict)
    cks = load_cookies()
    print(cks)