#utf-8
from pynput.keyboard import Listener
global LTMP
global RELEASE
global PRESS
LTMP = None
RELEASE = ""
PRESS = ""

def on_press(key):
    global PRESS
    try:
        #print("按下的是:" + key.char)
        PRESS = key.char
    except Exception as e:
        #print("按下的是:" + str(key))
        pass

def on_release(key):
    global LTMP
    global RELEASE
    try:
        #print("释放的是:" + key.char)
        RELEASE = key.char
    except Exception as e:
        #print("释放的是:" + str(key))
        pass
    if RELEASE == "=":
        LTMP.stop()

def _listen_s():
    global LTMP
    global RELEASE
    with Listener(on_press=on_press, on_release=on_release) as listener:
        LTMP = listener
        listener.join()
    return RELEASE