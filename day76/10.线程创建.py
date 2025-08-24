import time
from threading import Thread
def saySorry():
    print("亲爱的，我错了，我能吃饭了吗？")
    time.sleep(1)

if __name__ == "__main__":
    for i in range(5):
        t=Thread(target=saySorry)
        t.start()
    print('主线程结束')