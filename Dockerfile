FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# Tornar o script de lint executável
RUN chmod +x /code/lint.sh

CMD ["sh", "-c", "uvicorn app.main:app --host ${API_HOST} --port ${API_PORT} --reload"]
