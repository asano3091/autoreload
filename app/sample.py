import time
import os
import signal
import sys

print("Hello. I'm created. pid:{}".format(os.getpid()))

def handler(signum, frame):
    print("I'm killed. Bye. pid:{}".format(os.getpid()))
    sys.exit(0)
    pass

# SIGINT が発生した時の handler の登録
signal.signal(signal.SIGINT, handler)

while 1:
    time.sleep(1)
    