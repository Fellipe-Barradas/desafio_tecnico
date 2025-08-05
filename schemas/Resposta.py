from sqlmodel import SQLModel
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import RespostaModel


class RespostaBase(SQLModel):
    valor: str | None = None  # Para questões abertas
    alternativa_id: int | None = None  # Para questões de múltipla escolha
    questao_id: int
    usuario_id: int

class RespostaCreate(RespostaBase):
    pass

class RespostaUpdate(SQLModel):
    valor: str | None = None
    alternativa_id: int | None = None
    
class RespostaRead(RespostaBase):
    id: int | None = None
    valor: str | None = None
    alternativa_id: int | None = None
    questao_id: int
    usuario_id: int
    data_criacao: datetime
    data_modificacao: datetime
    
    @staticmethod
    def from_model(model: 'RespostaModel') -> 'RespostaRead':
        return RespostaRead(
            id=model.id,
            valor=model.valor,
            alternativa_id=model.alternativa_id,
            questao_id=model.questao_id,
            usuario_id=model.usuario_id,
            data_criacao=model.data_criacao,
            data_modificacao=model.data_modificacao
        )
