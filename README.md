# easy-backup
Script destinado a fazer Scan e back de Switchs L3 da Rede


--

# **Automação de Backup e Scan de Rede**

Este projeto consiste em dois scripts Python para automação de tarefas de rede:

1. **Scan de Rede e Armazenamento em JSON**:
   - Escaneia um bloco de IP (`10.0.0.0/24`) para identificar hosts ativos.
   - Conecta via SSH a novos hosts e coleta informações de configuração e interfaces ativas.
   - Armazena os dados no arquivo `banco-de-dados.json`.

2. **Backup de Configurações via SSH**:
   - Conecta via SSH a dispositivos listados no arquivo `banco-de-dados.json`.
   - Executa comandos para coletar a configuração e salva os backups em arquivos `.txt`.

---

## **Requisitos**

### **Dependências Python**
- **`paramiko`**: Conexão via SSH.
- **`json`**: Manipulação de arquivos JSON.
- **`os`**: Manipulação de diretórios e caminhos.
- **`subprocess`**: Execução de comandos externos (e.g., Nmap).
- **`datetime`**: Manipulação de datas.
- **`ipaddress`**: Validação de endereços IP.

### **Ferramenta Externa**
- **Nmap**: Utilizado para escanear a rede.

---

## **Instalação**

### **1. Dependências Python**
Certifique-se de que o Python 3.3 ou superior está instalado. Execute o comando abaixo para instalar a biblioteca necessária:
```bash
pip install paramiko
```

### **2. Instale o Nmap**
#### Linux (Ubuntu/Debian):
```bash
sudo apt install nmap
```

#### macOS:
```bash
brew install nmap
```

#### Windows:
Baixe e instale o Nmap no [site oficial](https://nmap.org/download.html).

### **3. Clone o Repositório**
```bash
git clone https://github.com/tayronroch/easy-backup.git
cd seu-repositorio
```

---

## **Uso**

### **1. Scan de Rede**
O script `scan-network.py` faz o escaneamento de dispositivos na rede, coleta informações e as salva no arquivo `banco-de-dados.json`.

#### **Execução:**
```bash
python scan-network.py
```

#### **Saída esperada:**
Um arquivo `banco-de-dados.json` será gerado no mesmo diretório do script, contendo informações dos dispositivos identificados, no formato:
```json
[
    {
        "name": "PI-TSA-PROVIDER-EDGE",
        "ip": "10.XXX.XXX.XX",
        "interfaces": [
            {
                "interface": "loopback",
                "ip": "10.XXX.XXX.XX",
                "state": "active"
            }
        ]
    }
]
```

---

### **2. Backup de Configurações**
O script `backup-config.py` conecta aos dispositivos listados no arquivo `banco-de-dados.json` e realiza o backup de configurações.

#### **Execução:**
```bash
python backup-config.py
```

#### **Saída esperada:**
Uma pasta de backup será criada no mesmo diretório do script com a data atual no formato `backup_YYYY-MM-DD`, e os arquivos `.txt` de backup serão salvos dentro dela.

Exemplo de estrutura gerada:
```
backup_2025-01-16/
├── PI-TSA-CE01-CLIENTE.txt
└── CE-FLA-XXXXXX-XXX.txt
```

---

## **Personalização**

### **Configuração SSH**
Edite as variáveis no início dos scripts para incluir as credenciais de SSH:
```python
USERNAME = "seu_usuario"
PASSWORD = "sua_senha"
SSH_PORT = 2222
```

### **Bloco de IP para Scan**
Altere o bloco de IP no arquivo `scan-network.py`:
```python
NETWORK = "10.XXX.XXX.0/24"
```

---

## **Contribuição**
Sinta-se à vontade para abrir _issues_ ou enviar _pull requests_ caso queira contribuir com o projeto.

---

## **Licença**
Este projeto é licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações."# easy-backup
