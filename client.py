#!/usr/bin/env python3

'''
pyforkexec client module.

usage: client.py <program_text>

to terminate the server, send an empty program text.
'''

import os
import socket
import sys

class pyforkexec_client:

    '''
    pyforkexec client class.

    the client connects to server via a stream-oriented unix domain socket. it
    sends the program text to server and then reads and displays stdout and
    stderr.
    '''

    def __init__(self):

        '''
        init the client.
        '''

        ##  socket name.
        self.socket = '/tmp/pyforkexec.sock'

        ##  header size (in bytes).
        self.hsize = 8

    def run(self):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            ##  connect to server.
            s.connect(self.socket)
            ##  send program text.
            pbytes = sys.argv[1].encode('utf-8')
            hbytes = len(pbytes).to_bytes(self.hsize, 'big')
            s.sendall(hbytes)
            s.sendall(pbytes)
            if not pbytes: sys.exit()
            rbytes = b''
            ##  read stdout size.
            while len(rbytes) < self.hsize:
                rbytes += s.recv(self.hsize)
            osize = int.from_bytes(rbytes[:self.hsize], 'big')
            rbytes = rbytes[self.hsize:]
            ##  read stdout.
            while len(rbytes) < osize:
                rbytes += s.recv(osize)
            stdout = rbytes[:osize].decode('utf-8')
            rbytes = rbytes[osize:]
            ##  read stderr size.
            while len(rbytes) < self.hsize:
                rbytes += s.recv(self.hsize)
            osize = int.from_bytes(rbytes[:self.hsize], 'big')
            rbytes = rbytes[self.hsize:]
            ##  read stderr.
            while len(rbytes) < osize:
                rbytes += s.recv(osize)
            stderr = rbytes[:osize].decode('utf-8')
            rbytes = rbytes[osize:]
            ##  write stdout.
            sys.stdout.write(stdout)
            ##  write stderr.
            sys.stderr.write(stderr)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('usage: {} <program_text>'.format(sys.argv[0]))
        sys.exit(1)

    client = pyforkexec_client()
    client.run()

