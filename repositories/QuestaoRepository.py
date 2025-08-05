from sqlmodel import Session, select, Sequence
from typing import Sequence
from models import QuestaoModel

class QuestaoRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100, somente_ativos: bool = True, formulario_id: int | None = None) -> Sequence[QuestaoModel]:
        query = select(QuestaoModel).offset(skip).limit(limit)
        if somente_ativos:
            query = query.where(QuestaoModel.ativo == True)
        if formulario_id is not None:
            query = query.where(QuestaoModel.formulario_id == formulario_id)
        questoes: Sequence[QuestaoModel] = self.session.exec(query).all()
        return questoes
    
    def get_by_id(self, questao_id: int) -> QuestaoModel | None:
        query = select(QuestaoModel).where(QuestaoModel.id == questao_id)
        return self.session.exec(query).one_or_none()
    
    def create(self, questao: QuestaoModel) -> QuestaoModel:
        self.session.add(questao)
        self.session.commit()
        self.session.refresh(questao)
        return questao
    
    def update(self, questao: QuestaoModel) -> QuestaoModel:
        self.session.add(questao)
        self.session.commit()
        self.session.refresh(questao)
        return questao
    
    def delete(self, questao_id: int) -> None:
        questao = self.get_by_id(questao_id)
        if questao:
            self.session.delete(questao)
            self.session.commit()
        else:
            raise ValueError("Questão not found")
