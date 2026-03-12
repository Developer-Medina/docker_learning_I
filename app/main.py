import os
import time
import random
import pymysql
from datetime import datetime

# COnexão com o BD com base no .env
def conectar():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

# Criando tb se não existir + cursor
def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras_miri (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperatura FLOAT NOT NULL,
            registrado_em DATETIME DEFAULT NOW()
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Funcao que valida se o intervalo da temperatura está de acordo
def checagem_temperatura(temp):
    if not isinstance(temp, (float, int)):
        print('[ERRO] A temperatura precisa ser um número.')
        return False
    elif 0 <= temp <= 100:
        return True
    print('[ERRO] Temperatura fora do intervalo válido (0-100K).')
    return False

# Decorator
def monitor_missao(funcao):
    total_leituras = 0

    def interna(*args, **kwargs):
        nonlocal total_leituras
        temp = args[0]

        if checagem_temperatura(temp):
            total_leituras += 1
            print(f'[TELEMETRIA] Leitura #{total_leituras} capturada com sucesso.')
            return funcao(*args, **kwargs)
        else:
            print('[ABORTADO] Sensor com falha — leitura descartada.')

    return interna

@monitor_missao
def registrar_miri(temp):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'[MIRI] Temperatura: {temp}K | Horário: {agora}')

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leituras_miri (temperatura) VALUES (%s)",
        (temp,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f'[DB] Registro salvo com sucesso.')


print('=' * 45)
print('JWST — Sistema de Monitoramento MIRI')
print('Iniciando sequência de telemetria...')
print('=' * 45)

inicializar_banco()
print('[DB] Banco de dados inicializado.')
print(f'[INFO] Intervalo entre leituras: 1 hora\n')

while True:
    temp = round(random.uniform(0.0, 100.0), 2)
    registrar_miri(temp)
    print(f'[INFO] Próxima leitura em 1 hora...\n')
    time.sleep(120)