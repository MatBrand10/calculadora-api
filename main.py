from pathlib import Path
from typing import Callable, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Calculadora API",
    description="API de Calculadora para Sistemas Distribuidos",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
UI_PATH = BASE_DIR / "static" / "index.html"


class OperacaoRequest(BaseModel):
    numero1: float
    numero2: float


class ResultadoResponse(BaseModel):
    operacao: str
    numero1: float
    numero2: float
    resultado: float


@app.get("/")
def home() -> Dict[str, str]:
    return {
        "mensagem": "Bem-vindo a Calculadora API!",
        "docs": "/docs",
        "ui": "/ui",
    }


@app.get("/ui")
def ui() -> FileResponse:
    if not UI_PATH.exists():
        raise HTTPException(status_code=404, detail="UI nao encontrada")
    return FileResponse(UI_PATH)


def _resultado(operacao: str, n1: float, n2: float, resultado: float) -> ResultadoResponse:
    return ResultadoResponse(
        operacao=operacao,
        numero1=n1,
        numero2=n2,
        resultado=resultado,
    )


def _dividir(n1: float, n2: float) -> float:
    if n2 == 0:
        raise HTTPException(status_code=400, detail="Divisao por zero nao e permitida")
    return n1 / n2


def _raiz(n1: float, n2: float) -> float:
    if n2 == 0:
        raise HTTPException(status_code=400, detail="Indice da raiz nao pode ser zero")
    if n1 < 0:
        if not float(n2).is_integer():
            raise HTTPException(
                status_code=400,
                detail="Raiz de numero negativo requer indice inteiro",
            )
        indice = int(n2)
        if indice % 2 == 0:
            raise HTTPException(
                status_code=400,
                detail="Raiz par de numero negativo nao e permitida",
            )
        return -((-n1) ** (1 / indice))
    return n1 ** (1 / n2)


@app.post("/somar", response_model=ResultadoResponse)
def somar(dados: OperacaoRequest) -> ResultadoResponse:
    return _resultado("soma", dados.numero1, dados.numero2, dados.numero1 + dados.numero2)


@app.post("/subtrair", response_model=ResultadoResponse)
def subtrair(dados: OperacaoRequest) -> ResultadoResponse:
    return _resultado("subtracao", dados.numero1, dados.numero2, dados.numero1 - dados.numero2)


@app.post("/multiplicar", response_model=ResultadoResponse)
def multiplicar(dados: OperacaoRequest) -> ResultadoResponse:
    return _resultado(
        "multiplicacao",
        dados.numero1,
        dados.numero2,
        dados.numero1 * dados.numero2,
    )


@app.post("/dividir", response_model=ResultadoResponse)
def dividir(dados: OperacaoRequest) -> ResultadoResponse:
    resultado = _dividir(dados.numero1, dados.numero2)
    return _resultado("divisao", dados.numero1, dados.numero2, resultado)


@app.post("/potencia", response_model=ResultadoResponse)
def potencia(dados: OperacaoRequest) -> ResultadoResponse:
    return _resultado("potencia", dados.numero1, dados.numero2, dados.numero1 ** dados.numero2)


@app.post("/raiz", response_model=ResultadoResponse)
def raiz_operacao(dados: OperacaoRequest) -> ResultadoResponse:
    resultado = _raiz(dados.numero1, dados.numero2)
    return _resultado("raiz", dados.numero1, dados.numero2, resultado)


def _operacoes() -> Dict[str, Callable[[float, float], float]]:
    return {
        "soma": lambda a, b: a + b,
        "subtracao": lambda a, b: a - b,
        "multiplicacao": lambda a, b: a * b,
        "divisao": _dividir,
        "potencia": lambda a, b: a ** b,
        "raiz": _raiz,
    }


@app.get("/calcular")
def calcular_query(numero1: float, numero2: float, operacao: str) -> Dict[str, float | str]:
    operacoes = _operacoes()
    if operacao not in operacoes:
        raise HTTPException(
            status_code=400,
            detail=f"Operacao invalida. Use: {list(operacoes.keys())}",
        )
    resultado = operacoes[operacao](numero1, numero2)
    return {
        "operacao": operacao,
        "numero1": numero1,
        "numero2": numero2,
        "resultado": resultado,
    }
