from sqlmodel import SQLModel
from datetime import datetime
from models import FormularioModel

class FormularioBase(SQLModel):
    titulo: str
    descricao: str
    ativo: bool = True
    
class FormularioCreate(FormularioBase):
    pass

class FormularioUpdate(FormularioBase):
    titulo: str | None = None
    descricao: str | None = None
    ativo: bool | None = None
    
class FormularioRead(FormularioBase):
    id: int
    titulo: str
    descricao: str
    ativo: bool
    data_criacao: datetime
    data_modificacao: datetime
    data_desativacao: datetime | None = None
    
    @staticmethod
    def from_orm(model: 'FormularioModel') -> 'FormularioRead':
        return FormularioRead(
            id=model.id,
            titulo=model.titulo,
            descricao=model.descricao,
            ativo=model.ativo,
            data_criacao=model.data_criacao,
            data_modificacao=model.data_modificacao,
            data_desativacao=model.data_desativacao
        )