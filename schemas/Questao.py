from sqlmodel import SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import QuestaoModel


class QuestaoBase(SQLModel):
    enunciado: str
    tipo: str
    ativo: bool = True
    formulario_id: int

class QuestaoCreate(QuestaoBase):
    pass

class QuestaoUpdate(SQLModel):
    enunciado: str | None = None
    tipo: str | None = None
    ativo: bool | None = None
    
class QuestaoRead(QuestaoBase):
    id: int | None = None
    enunciado: str
    tipo: str
    ativo: bool = True
    formulario_id: int
    
    @staticmethod
    def from_model(model: 'QuestaoModel') -> 'QuestaoRead':
        return QuestaoRead(
            id=model.id,
            enunciado=model.enunciado,
            tipo=model.tipo,
            ativo=model.ativo,
            formulario_id=model.formulario_id
        )