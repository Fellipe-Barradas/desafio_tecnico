from schemas import QuestaoBase
from sqlmodel import Field

class QuestaoModel(QuestaoBase, table=True):
    __tablename__ = "questoes"  # type: ignore
    
    id: int | None = Field(default=None, primary_key=True)
    enunciado: str = Field(..., max_length=1000)
    tipo: str = Field(..., max_length=50)
    ativo: bool = Field(default=True)
    formulario_id: int = Field(foreign_key="formularios.id")
    