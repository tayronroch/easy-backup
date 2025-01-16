import paramiko
import json
import os
from datetime import datetime

# Configurações SSH
USERNAME = "login"  # Substitua pelo nome de usuário
PASSWORD = "senha"  # Substitua pela senha
SSH_PORT = 2222  # Porta SSH
COMMAND = "show running-config | nomore"  # Comando a ser executado

# Nome do arquivo JSON com os dispositivos
JSON_FILE = "banco-de-dados.json"

# Diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório de backup com data
DATE = datetime.now().strftime("%Y-%m-%d")
BACKUP_DIR = os.path.join(SCRIPT_DIR, f"backup_{DATE}")
os.makedirs(BACKUP_DIR, exist_ok=True)  # Cria a pasta se não existir

# Função para carregar dispositivos do JSON
def load_devices_from_json(json_file):
    try:
        json_path = os.path.join(SCRIPT_DIR, json_file)  # Garante que o JSON esteja no mesmo local do script
        if not os.path.exists(json_path):
            print(f"Arquivo JSON {json_path} não encontrado.")
            return []
        with open(json_path, "r", encoding="utf-8") as file:
            devices = json.load(file)
            print(f"{len(devices)} dispositivos carregados do arquivo {json_path}.")
            return devices
    except json.JSONDecodeError as e:
        print(f"Erro ao ler o arquivo JSON {json_file}: {e}")
        return []

# Função para executar o comando via SSH
def execute_ssh_command(device):
    try:
        print(f"Conectando ao dispositivo {device['name']} ({device['ip']})...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Aceita chaves automaticamente
        client.connect(
            device["ip"], port=SSH_PORT, username=USERNAME, password=PASSWORD, timeout=10
        )

        # Executa o comando
        print(f"Executando comando: {COMMAND}")
        stdin, stdout, stderr = client.exec_command(COMMAND)
        output = stdout.read().decode("utf-8")  # Lê e decodifica a saída

        # Salva a saída em um arquivo .txt na pasta correta
        file_name = os.path.join(BACKUP_DIR, f"{device['name']}.txt")
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(output)
        print(f"Configuração salva em {file_name}")

    except paramiko.AuthenticationException:
        print(f"Falha na autenticação para {device['name']} ({device['ip']}).")
    except paramiko.SSHException as e:
        print(f"Erro ao conectar ao dispositivo {device['name']} ({device['ip']}): {e}")
    except Exception as e:
        print(f"Erro inesperado com {device['name']} ({device['ip']}): {e}")
    finally:
        client.close()
        print(f"Conexão com {device['name']} encerrada.\n")

# Itera sobre a lista de dispositivos
def backup_running_config(devices):
    for device in devices:
        execute_ssh_command(device)

if __name__ == "__main__":
    print(f"Iniciando backup das configurações no diretório: {BACKUP_DIR}")
    devices = load_devices_from_json(JSON_FILE)
    if devices:
        backup_running_config(devices)
        print("Backup concluído.")
    else:
        print("Nenhum dispositivo encontrado para realizar o backup.")
