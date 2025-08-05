from schemas import RespostaBase
from sqlmodel import Field
from datetime import datetime

class RespostaModel(RespostaBase, table=True):
    __tablename__ = "respostas"  # type: ignore
    
    id: int | None = Field(default=None, primary_key=True)
    valor: str | None = Field(default=None, max_length=2000)  # Para questões abertas
    alternativa_id: int | None = Field(default=None, foreign_key="alternativas.id")  # Para múltipla escolha
    questao_id: int = Field(foreign_key="questoes.id")
    usuario_id: int = Field(foreign_key="usuarios.id")
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_modificacao: datetime = Field(default_factory=datetime.now)
