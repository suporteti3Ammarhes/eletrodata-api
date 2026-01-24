from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Consulta:
    nome: str
    sentenca: str
    parametros_fixos: str
    campos: List[str]
    requer_periodo: bool
    processar_status: bool = False
    table: str = ""
    campo_referencia: str = ""


@dataclass
class ResultadoConsulta:
    consulta: str
    sentenca: str
    parametros: str
    total_registros: int
    dados: List[Dict[str, Any]]
    timestamp: str
