from schemas import AlternativaBase
from sqlmodel import Field

class AlternativaModel(AlternativaBase, table=True):
    __tablename__ = "alternativas"  # type: ignore
    
    id: int | None = Field(default=None, primary_key=True)
    texto: str = Field(..., max_length=500)
    correta: bool = Field(default=False)
    ativo: bool = Field(default=True)
    questao_id: int = Field(foreign_key="questoes.id")
