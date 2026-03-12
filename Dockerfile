# Começa com uma máquina que já tem o Python 3.14 instalado
FROM python:3.14-slim    

# ENV
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Vamos copiar nosso arquivo de requerimentos e já instalar, aqui no topo mesmo!
COPY requirements.txt .
RUN pip install -r requirements.txt

# Agora sim: trabalhe na pasta /app. Se ela não existir, crie
WORKDIR /app             

# Pega o arquivo main.py da minha máquina e copie ele aqui
COPY app/main.py .

# Quando o container inciiar,roda o python main.py
CMD ["python", "main.py"]