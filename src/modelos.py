from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Colaborador:
    id: str
    nome: str
    centro_custo: str


@dataclass(frozen=True)
class Periodo:
    competencia: str
    inicio: date
    fim: date


@dataclass(frozen=True)
class DespesaBruta:
    id: str
    data: date
    categoria: str
    descricao: str
    fornecedor: str
    valor_original: Decimal
    tem_nota_fiscal: bool


@dataclass(frozen=True)
class Despesa:
    id: str
    data: date
    categoria: str
    descricao: str
    fornecedor: str
    valor_original: Decimal
    valor_considerado: Decimal
    tem_nota_fiscal: bool


@dataclass(frozen=True)
class ResultadoItem:
    id: str
    status: str
    valor_original: Decimal
    valor_considerado: Decimal
    valor_reembolsavel: Decimal
    motivo_codigo: str | None
    motivo_texto: str | None
    duplicata_de: str | None


@dataclass(frozen=True)
class Resumo:
    total_solicitado: Decimal
    total_reembolsavel: Decimal
    total_recusado: Decimal
    itens_processados: int
    itens_aprovados: int
    itens_parciais: int
    itens_recusados: int


@dataclass(frozen=True)
class Resultado:
    colaborador: Colaborador
    periodo: Periodo
    resumo: Resumo
    itens: tuple[ResultadoItem, ...]
