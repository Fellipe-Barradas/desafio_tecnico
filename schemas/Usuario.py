from sqlmodel import SQLModel
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import UsuarioModel

class UsuarioBase(SQLModel):
    nome: str
    email: str
    ativo: bool = True
    
class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(SQLModel):
    nome: str | None = None
    email: str | None = None
    ativo: bool | None = None
    senha: str | None = None

class UsuarioRead(UsuarioBase):
    id: int | None = None
    nome: str
    email: str
    ativo: bool = True
    data_criacao: datetime
    data_modificacao: datetime
    data_desativacao: datetime | None = None
    
    @staticmethod
    def from_usuario_model(model: 'UsuarioModel') -> 'UsuarioRead':
        return UsuarioRead(
            id=model.id,
            nome=model.nome,
            email=model.email,
            ativo=model.ativo,
            data_criacao=model.data_criacao,
            data_modificacao=model.data_modificacao,
            data_desativacao=model.data_desativacao
        )