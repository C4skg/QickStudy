import time

def getTime()-> str:
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());