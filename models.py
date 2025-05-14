"""
Models - Classes de domínio para o sistema Kanban
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Protocol


class Observer(Protocol):
    """Interface para o padrão Observer"""
    def update(self, event: str, data: dict = None):
        """Método chamado quando há mudanças nos dados"""
        ...


class Observable:
    """Classe base para objetos observáveis"""
    def __init__(self):
        self._observers: List[Observer] = []
    
    def add_observer(self, observer: Observer):
        """Adiciona um observador"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: Observer):
        """Remove um observador"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: str, data: dict = None):
        """Notifica todos os observadores sobre uma mudança"""
        for observer in self._observers:
            observer.update(event, data)


@dataclass
class Etapa:
    """Representa uma etapa do Kanban"""
    id: int
    nome: str
    ordem: int
    
    def __str__(self):
        return self.nome


@dataclass
class Faturamento:
    """Representa um faturamento de projeto"""
    id: Optional[int]
    projeto_id: int
    valor: Decimal
    descricao: Optional[str]
    data_faturamento: datetime
    data_criacao: Optional[datetime] = None
    
    def __str__(self):
        return f"{self.descricao or 'Faturamento'} - R$ {self.valor}"


@dataclass
class Projeto:
    """Representa um projeto no sistema"""
    id: Optional[int]
    nome: str
    descricao: Optional[str]
    pasta_local: Optional[str]
    arquivo_principal: Optional[str]
    etapa_atual: int
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    receita_total: Decimal = Decimal('0.00')
    faturamentos: List[Faturamento] = None
    
    def __post_init__(self):
        if self.faturamentos is None:
            self.faturamentos = []
    
    def __str__(self):
        return self.nome
    
    def adicionar_faturamento(self, faturamento: Faturamento):
        """Adiciona um faturamento ao projeto"""
        self.faturamentos.append(faturamento)
        self.receita_total += faturamento.valor