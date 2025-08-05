from schemas import FormularioBase
from sqlmodel import Field
from datetime import datetime

class FormularioModel(FormularioBase, table=True):
    __tablename__ = "formularios" # type: ignore
    
    id: int | None = Field(default=None, primary_key=True, index=True)
    titulo: str = Field(..., max_length=255)
    descricao: str = Field(..., max_length=1000)
    ativo: bool = Field(default=True)
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_modificacao: datetime = Field(default_factory=datetime.now)
    data_desativacao: datetime | None = Field(default=None)
    usuario_id: int = Field(foreign_key="usuarios.id")
