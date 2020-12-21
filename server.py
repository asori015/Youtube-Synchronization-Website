#!/usr/bin/env python3

import socket
import threading
import datetime as dt
import os
import time


def MakeHTTPHeader(fileType, fileSize):
    timestamp = dt.datetime.utcnow().ctime().split()
    html = b'HTTP/1.1 200 OK\r\n'
    html += str.encode('Date: ' + timestamp[0] + ', ' + timestamp[2] + ' '
        + timestamp[1] + ' ' + timestamp[4] + ' ' + timestamp[3] + ' GMT\r\n')
    html += str.encode('Content-Type: text/' + fileType + '\r\n')
    html += str.encode('Content-Length: ' + str(fileSize) + '\r\n')
    html += b'\r\n'
    return html

def ServeHTTPToClient(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            request = data.decode("utf-8").split("\r\n")
            firstLine = request[0].split()
            if firstLine[0] == 'GET':
                if(firstLine[1] == '/'):
                    firstLine[1] = '/test.html'
                resource = open(os.getcwd() + firstLine[1], 'rb').read()
                conn.sendall(MakeHTTPHeader(firstLine[1].split('.')[1], len(resource)) + resource)
        print('Done serving.')

def MakeThread(conn, addr):
    serverThread = threading.Thread(target=ServeHTTPToClient, args=(conn, addr,))
    serverThread.start()
    if(threading.current_thread() != threading.main_thread()):
        print(threading.active_count())
        threading.current_thread().join()

def StartServer():
    HOST, PORT = "localhost", 9999
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    while True:
        conn, addr = serverSocket.accept()
        MakeThread(conn, addr)

if __name__ == "__main__":
    StartServer()
