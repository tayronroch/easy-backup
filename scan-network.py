import paramiko
import json
import os
import subprocess
import ipaddress

# Diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, "banco-de-dados.json")  # Nome do arquivo JSON

# Configurações
NETWORK = "10.0.0.0/8"  # Bloco de IP a ser escaneado
USERNAME = "login"  # Substitua pelo nome de usuário
PASSWORD = "senha"  # Substitua pela senha
SSH_PORT = 2222  # Porta SSH
JSON_FILE = "banco-de-dados.json"  # Nome do arquivo JSON

# Diretório do script e JSON na mesma pasta
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, "banco-de-dados.json")  # Caminho do arquivo JSON

# Função para escanear a rede
def scan_network(network):
    print(f"Escaneando a rede {network}...")
    try:
        result = subprocess.run(
            ["nmap", "-p", str(SSH_PORT), "-n", "-oG", "-", network],
            capture_output=True,
            text=True,
        )
        active_hosts = []
        for line in result.stdout.splitlines():
            if "open" in line and not line.startswith("#"):
                parts = line.split()
                active_hosts.append(parts[1])
        # Filtra hosts válidos
        active_hosts = [
            ip for ip in active_hosts if ipaddress.ip_address(ip).is_private
            and not ip.endswith(".0")  # Remove endereços de rede
            and not ip.endswith(".255")  # Remove endereços de broadcast
        ]
        print(f"Hosts ativos encontrados: {active_hosts}")
        return active_hosts
    except Exception as e:
        print(f"Erro ao escanear a rede: {e}")
        return []

# Função para verificar se o host já está registrado
def is_host_registered(ip, json_file):
    if not os.path.exists(json_file):
        return False
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        return any(host["ip"] == ip for host in data)

# Função para coletar informações do host via SSH
# Função para coletar informações do host via SSH
def collect_host_info(ip):
    try:
        print(f"Conectando ao host {ip}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=SSH_PORT, username=USERNAME, password=PASSWORD, timeout=10)

        # Executa o comando 1: show running-config hostname
        stdin, stdout, stderr = client.exec_command("show running-config hostname")
        hostname_output = stdout.read().decode("utf-8").strip()
        hostname = None
        for line in hostname_output.splitlines():
            if line.startswith("hostname"):
                hostname = line.split()[1]

        # Executa o comando 2: show ip interface brief
        stdin, stdout, stderr = client.exec_command("show ip interface brief")
        interfaces_output = stdout.read().decode("utf-8").strip()
        interfaces = []
        for line in interfaces_output.splitlines():
            if "active" in line:  # Filtra apenas interfaces ativas
                parts = line.split()
                if len(parts) >= 4:
                    # Exclui interfaces com IPs "4000" ou "4001"
                    if parts[3] not in ["4000", "4001", "4002", "4003", "loopback-0", "100", "98"]:  
                        interfaces.append({"interface": parts[1], "ip": parts[3], "state": parts[-1]})

        client.close()
        return {"name": hostname, "ip": ip, "interfaces": interfaces}

    except Exception as e:
        print(f"Erro ao coletar informações do host {ip}: {e}")
        return None

# Função para atualizar o arquivo JSON
def update_json(data, json_file):
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Adiciona os novos dados e remove duplicatas pelo IP
    updated_data = {item["ip"]: item for item in (existing_data + data)}.values()

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(list(updated_data), file, indent=4)
    print(f"Arquivo JSON atualizado: {json_file}")

# Função principal
def main():
    # Escaneia a rede
    active_hosts = scan_network(NETWORK)

    # Lista para armazenar novos hosts
    new_hosts = []

    for ip in active_hosts:
        if not is_host_registered(ip, JSON_FILE):
            print(f"Host novo encontrado: {ip}")
            host_info = collect_host_info(ip)
            if host_info:
                new_hosts.append(host_info)

    if new_hosts:
        update_json(new_hosts, JSON_FILE)
    else:
        print("Nenhum host novo encontrado.")

if __name__ == "__main__":
    main()
