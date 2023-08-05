#utf-8
from . import key_listen

def listen_s():
    release = key_listen._listen_s()
    if release == "=":
        print("Find it!!!")