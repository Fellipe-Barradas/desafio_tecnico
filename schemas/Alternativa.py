from sqlmodel import SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import AlternativaModel


class AlternativaBase(SQLModel):
    texto: str
    correta: bool = False
    ativo: bool = True
    questao_id: int

class AlternativaCreate(AlternativaBase):
    pass

class AlternativaUpdate(SQLModel):
    texto: str | None = None
    correta: bool | None = None
    ativo: bool | None = None
    
class AlternativaRead(AlternativaBase):
    id: int | None = None
    texto: str
    correta: bool = False
    ativo: bool = True
    questao_id: int
    
    @staticmethod
    def from_model(model: 'AlternativaModel') -> 'AlternativaRead':
        return AlternativaRead(
            id=model.id,
            texto=model.texto,
            correta=model.correta,
            ativo=model.ativo,
            questao_id=model.questao_id
        )
