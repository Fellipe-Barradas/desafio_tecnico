from schemas import UsuarioBase
from sqlmodel import Field
from datetime import datetime

class UsuarioModel(UsuarioBase, table=True):
    __tablename__ = "usuarios"  # type: ignore
    
    id: int | None = Field(default=None, primary_key=True)
    senha: str = Field(..., max_length=255)
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_modificacao: datetime = Field(default_factory=datetime.now)
    data_desativacao: datetime | None = Field(default=None)

