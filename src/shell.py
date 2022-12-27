import tornado.web
from src.config import cookie_data
import json
from subprocess import Popen, PIPE
import threading

shell_pipe = Popen('powershell', stdout=PIPE, stdin=PIPE)

shell_buffer = []


def reader(f, buffer):
    while True:
        line = f.readline()
        if line:
            buffer.append(line)
        else:
            break


shell_pipe_reading_thread = threading.Thread(
    target=reader, args=[shell_pipe.stdout, shell_buffer])
shell_pipe_reading_thread.daemon = True
shell_pipe_reading_thread.start()


class shell(tornado.web.RequestHandler):
    def post(self, *keys):
        if self.get_cookie('auth') not in cookie_data:
            return
        cmd = json.loads(self.request.body.decode())['cmd']
        shell_pipe.stdin.write(cmd.encode())
        shell_pipe.stdin.flush()
        if len(shell_buffer) != 0:
            self.write(''.join(x.decode()for x in shell_buffer))
            shell_buffer.clear()
