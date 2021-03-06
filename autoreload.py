#!/usr/bin/env python
import os
import sys
import subprocess
import time
import signal

def file_filter(name):
    return (name.endswith(".py") and not ("autoreload.py" in name))

def file_times(path):
    for top_level in os.listdir(path):
        if not os.path.isdir(top_level) and file_filter(top_level ):
            yield os.stat(top_level).st_mtime
        for root, dirs, files in os.walk(top_level):
            for file in filter(file_filter, files):
                yield os.stat(os.path.join(root, file)).st_mtime


def print_stdout(process):
    stdout = process.stdout
    if stdout != None:
        print(stdout)


# We concatenate all of the arguments together, and treat that as the command to run
command = ' '.join(sys.argv[1:])

# The path to watch
path = '.'

# How often we check the filesystem for changes (in seconds)
wait = 1

# The process to autoreload
process = subprocess.Popen(command.split(" "))

# The current maximum file modified time under the watched directory
last_mtime = max(file_times(path))
while True:
    max_mtime = max(file_times(path))
    print_stdout(process)
    if max_mtime > last_mtime:
        last_mtime = max_mtime
        print ('## Restarting process on file change ! ##')
        os.kill(process.pid, signal.SIGINT)
        process = subprocess.Popen(command.split(" "))
    time.sleep(wait)
