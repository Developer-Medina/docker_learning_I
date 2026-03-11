import os
import pymysql

# Estamos lendo as vars de ambiente do .env
host     = os.environ.get("DB_HOST")
database = os.environ.get("DB_NAME")
user     = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")

# Conexao com o bd
conexao = pymysql.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

print("Conectado com sucesso!")

# Para executar um comando SQL, precisamos de um cursor - e já vamos criar ele aqui
cursor = conexao.cursor()

# Criando a tabela caso não exista
cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        mensagem VARCHAR(255),
        criado_em DATETIME DEFAULT NOW()
    )
""")

# Insert
cursor.execute("INSERT INTO log (mensagem) VALUES ('script rodou!')")

# Commita - transacional, então precisa da confirmação
conexao.commit()

print("Registro inserido com sucesso!")

# Fecha a conexão
cursor.close()
conexao.close()