from sqlmodel import Session, select
from typing import Sequence
from models import RespostaModel

class RespostaRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100, usuario_id: int | None = None, questao_id: int | None = None, alternativa_id: int | None = None) -> Sequence[RespostaModel]:
        query = select(RespostaModel).offset(skip).limit(limit)
        if usuario_id is not None:
            query = query.where(RespostaModel.usuario_id == usuario_id)
        if questao_id is not None:
            query = query.where(RespostaModel.questao_id == questao_id)
        if alternativa_id is not None:
            query = query.where(RespostaModel.alternativa_id == alternativa_id)
        respostas: Sequence[RespostaModel] = self.session.exec(query).all()
        return respostas
    
    def get_by_id(self, resposta_id: int) -> RespostaModel | None:
        query = select(RespostaModel).where(RespostaModel.id == resposta_id)
        return self.session.exec(query).one_or_none()
    
    def get_by_usuario_and_questao(self, usuario_id: int, questao_id: int) -> RespostaModel | None:
        query = select(RespostaModel).where(
            RespostaModel.usuario_id == usuario_id,
            RespostaModel.questao_id == questao_id
        )
        return self.session.exec(query).one_or_none()
    
    def get_by_usuario_id(self, usuario_id: int) -> Sequence[RespostaModel]:
        query = select(RespostaModel).where(RespostaModel.usuario_id == usuario_id)
        respostas: Sequence[RespostaModel] = self.session.exec(query).all()
        return respostas
    
    def get_by_questao_id(self, questao_id: int) -> Sequence[RespostaModel]:
        query = select(RespostaModel).where(RespostaModel.questao_id == questao_id)
        respostas: Sequence[RespostaModel] = self.session.exec(query).all()
        return respostas
    
    def get_by_alternativa_id(self, alternativa_id: int) -> Sequence[RespostaModel]:
        query = select(RespostaModel).where(RespostaModel.alternativa_id == alternativa_id)
        respostas: Sequence[RespostaModel] = self.session.exec(query).all()
        return respostas
    
    def create(self, resposta: RespostaModel) -> RespostaModel:
        self.session.add(resposta)
        self.session.commit()
        self.session.refresh(resposta)
        return resposta
    
    def update(self, resposta: RespostaModel) -> RespostaModel:
        self.session.add(resposta)
        self.session.commit()
        self.session.refresh(resposta)
        return resposta
    
    def delete(self, resposta_id: int) -> None:
        resposta = self.get_by_id(resposta_id)
        if resposta:
            self.session.delete(resposta)
            self.session.commit()
        else:
            raise ValueError("Resposta not found")
