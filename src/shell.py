import tornado.web
from src.config import cookie_data
import json
from subprocess import Popen, PIPE
import threading
import os
import sys

# shell pipe to execute shell command


def reader(f, buffer):
    while True:
        line = f.readline()
        if line:
            buffer.append(line)
        else:
            break


def start_shell():

    if os.name == 'nt':
        # windows
        shell_pipe = Popen('powershell', stdout=PIPE, stdin=PIPE)
    else:
        # linux
        shell_pipe = Popen(['/bin/bash', '-c', cmd], stdout=PIPE, stdin=PIPE)
    shell_buffer = []
    shell_pipe_reading_thread = threading.Thread(
        target=reader, args=[shell_pipe.stdout, shell_buffer])
    shell_pipe_reading_thread.daemon = True
    shell_pipe_reading_thread.start()
    shell_pipe.stop = sys.exit
    shell_pipe.stopped = False
    return shell_pipe, shell_pipe_reading_thread, shell_buffer


class shell(tornado.web.RequestHandler):
    def post(self, *keys):
        if self.get_cookie('auth') not in cookie_data:
            return
        cmd = json.loads(self.request.body.decode())['cmd']
        if cmd == 'exit':
            shell_pipe.stop(0)
            return
        shell_pipe.stdin.write(cmd.encode())
        shell_pipe.stdin.flush()
        if len(shell_buffer) != 0:
            self.write(''.join(x.decode()for x in shell_buffer))
            shell_buffer.clear()


# start shell pipe, expose shell output buffer
shell_pipe, shell_pipe_reading_thread, shell_buffer = start_shell()
