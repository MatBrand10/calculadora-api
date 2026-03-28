import json
import urllib.request

BASE_URL = "http://localhost:8000"


def post(endpoint: str, dados: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(dados).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


# Testar todas as operacoes
r = post("/somar", {"numero1": 10, "numero2": 5})
print(f"Soma: {r['resultado']}")  # 15.0

r = post("/subtrair", {"numero1": 10, "numero2": 3})
print(f"Subtracao: {r['resultado']}")  # 7.0

r = post("/multiplicar", {"numero1": 4, "numero2": 5})
print(f"Multiplicacao: {r['resultado']}")  # 20.0

r = post("/dividir", {"numero1": 10, "numero2": 2})
print(f"Divisao: {r['resultado']}")  # 5.0

r = post("/potencia", {"numero1": 2, "numero2": 3})
print(f"Potencia: {r['resultado']}")  # 8.0

r = post("/raiz", {"numero1": 27, "numero2": 3})
print(f"Raiz: {r['resultado']}")  # 3.0
