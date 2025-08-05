from sqlmodel import SQLModel
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import FormularioModel

class FormularioBase(SQLModel):
    titulo: str
    descricao: str
    ativo: bool = True
    usuario_id: int    
class FormularioCreate(FormularioBase):
    pass

class FormularioUpdate(SQLModel):
    titulo: str | None = None
    descricao: str | None = None
    ativo: bool | None = None
    
class FormularioRead(FormularioBase):
    id: int | None = None
    titulo: str
    descricao: str
    ativo: bool = True
    usuario_id: int
    data_criacao: datetime
    data_modificacao: datetime
    data_desativacao: datetime | None = None
    
    @staticmethod
    def from_model(model: 'FormularioModel') -> 'FormularioRead':
        return FormularioRead(
            id=model.id,
            titulo=model.titulo,
            descricao=model.descricao,
            ativo=model.ativo,
            usuario_id=model.usuario_id,
            data_criacao=model.data_criacao,
            data_modificacao=model.data_modificacao,
            data_desativacao=model.data_desativacao
        )