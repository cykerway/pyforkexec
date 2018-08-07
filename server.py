#!/usr/bin/env python3

'''
pyforkexec server module.

usage: server.py [program_text]
'''

##  init user script.
import sys as pyforkexec_sys
if len(pyforkexec_sys.argv) > 1:
    exec(pyforkexec_sys.argv[1])

##  save global and local symbol tables.
pyforkexec_globals = globals()
pyforkexec_locals = locals()

import os
import socket
import sys

class pyforkexec_wrapfile:
    '''
    a file object wrapper which writes to str.
    '''

    def __init__(self, f):
        self.f = f
        self.buf = ''

    def __getattr__(self, attr):
         return getattr(self.f, attr)

    def write(self, data):
        self.buf += data
        return len(data)

class pyforkexec_server:

    '''
    pyforkexec server class.

    the server listens on a stream-oriented unix domain socket. whenever a
    connection is made to the server, the server accepts it, reads the program
    and runs the program in a forked process. the output is buffered in a str
    and sent back to client after the program is finished.

    the server terminates on empty input.
    '''

    def __init__(self):

        '''
        init the server.
        '''

        ##  socket name.
        self.socket = '/tmp/pyforkexec.sock'

        ##  header size (in bytes).
        self.hsize = 8

    def run(self):

        '''
        run the server.
        '''

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            ##  bind to socket.
            os.path.exists(self.socket) and os.remove(self.socket)
            s.bind(self.socket)
            ##  listen on socket.
            s.listen()
            while True:
                ##  accept connection.
                s2, _ = s.accept()
                with s2:
                    ##  init recv buffer.
                    rbytes = b''
                    ##  read input size.
                    while len(rbytes) < self.hsize:
                        rbytes += s2.recv(self.hsize)
                    isize = int.from_bytes(rbytes[:self.hsize], 'big')
                    rbytes = rbytes[self.hsize:]
                    ##  break if input is empty.
                    if isize == 0: break
                    ##  read input.
                    while len(rbytes) < isize:
                        rbytes += s2.recv(isize)
                    ##  fork.
                    if os.fork() == 0:
                        ##  redirect stdout and stderr.
                        sys.stdout = pyforkexec_wrapfile(open('/dev/null', 'w'))
                        sys.stderr = pyforkexec_wrapfile(open('/dev/null', 'w'))
                        ##  run user script.
                        try:
                            exec(rbytes.decode('utf-8'),
                                 pyforkexec_globals,
                                 pyforkexec_locals)
                        except Exception as e:
                            sys.stderr.buf = str(e) + '\n'
                        ##  send stdout.
                        obytes = sys.stdout.buf.encode('utf-8')
                        hbytes = len(obytes).to_bytes(self.hsize, 'big')
                        s2.sendall(hbytes)
                        s2.sendall(obytes)
                        ##  send stderr.
                        obytes = sys.stderr.buf.encode('utf-8')
                        hbytes = len(obytes).to_bytes(self.hsize, 'big')
                        s2.sendall(hbytes)
                        s2.sendall(obytes)
                        ##  break.
                        break

if __name__ == '__main__':

    server = pyforkexec_server()
    server.run()

