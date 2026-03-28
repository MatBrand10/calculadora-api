# Calculadora API com FastAPI

Projeto avaliativo da disciplina de Sistemas Distribuidos. Esta API realiza operacoes matematicas via endpoints REST e inclui um frontend simples para consumo dos endpoints.

**Projeto Avaliativo desenvolvido para disciplina Programação de Sistemas Distribuidos da Universidade do Grandes Lagos - UNILAGO sob supervisão do Professor Gleydes Oliveira**

## Requisitos

- Python 3.12+
- Pip

## Instalar dependencias

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Executar a API

```bash
uvicorn main:app --reload
```

Acesse:

- Documentacao Swagger: http://localhost:8000/docs
- UI do projeto: http://localhost:8000/ui

## Endpoints principais

- GET `/`
- POST `/somar`
- POST `/subtrair`
- POST `/multiplicar`
- POST `/dividir`
- POST `/potencia`
- POST `/raiz`
- GET `/calcular?numero1=&numero2=&operacao=`

### Exemplo (POST)

```bash
curl -X POST "http://localhost:8000/somar" \
  -H "Content-Type: application/json" \
  -d '{"numero1": 10, "numero2": 5}'
```

## Frontend

O frontend esta em `static/index.html` e pode ser acessado em `http://localhost:8000/ui` com o servidor rodando.

## Testes rapidos

Com o servidor rodando:

```bash
python test_client.py
```

## Estrutura do projeto

```
calculadora-api/
|-- main.py
|-- requirements.txt
|-- test_client.py
|-- static/
|   |-- index.html
```
