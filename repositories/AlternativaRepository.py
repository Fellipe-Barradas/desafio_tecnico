from sqlmodel import Session, select
from typing import Sequence
from models import AlternativaModel

class AlternativaRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100, somente_ativos: bool = True, questao_id: int | None = None) -> Sequence[AlternativaModel]:
        query = select(AlternativaModel).offset(skip).limit(limit)
        if somente_ativos:
            query = query.where(AlternativaModel.ativo == True)
        if questao_id is not None:
            query = query.where(AlternativaModel.questao_id == questao_id)
        alternativas: Sequence[AlternativaModel] = self.session.exec(query).all()
        return alternativas
    
    def get_by_id(self, alternativa_id: int) -> AlternativaModel | None:
        query = select(AlternativaModel).where(AlternativaModel.id == alternativa_id)
        return self.session.exec(query).one_or_none()
    
    def get_by_questao_id(self, questao_id: int, somente_ativos: bool = True) -> Sequence[AlternativaModel]:
        query = select(AlternativaModel).where(AlternativaModel.questao_id == questao_id)
        if somente_ativos:
            query = query.where(AlternativaModel.ativo == True)
        alternativas: Sequence[AlternativaModel] = self.session.exec(query).all()
        return alternativas
    
    def create(self, alternativa: AlternativaModel) -> AlternativaModel:
        self.session.add(alternativa)
        self.session.commit()
        self.session.refresh(alternativa)
        return alternativa
    
    def update(self, alternativa: AlternativaModel) -> AlternativaModel:
        self.session.add(alternativa)
        self.session.commit()
        self.session.refresh(alternativa)
        return alternativa
    
    def delete(self, alternativa_id: int) -> None:
        alternativa = self.get_by_id(alternativa_id)
        if alternativa:
            self.session.delete(alternativa)
            self.session.commit()
        else:
            raise ValueError("Alternativa not found")
