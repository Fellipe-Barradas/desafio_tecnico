from fastapi import Depends
from sqlmodel import Session
from config import get_session
from repositories import FormularioRepository, UsuarioRepository, QuestaoRepository, AlternativaRepository, RespostaRepository

def get_formulario_repository(session: Session = Depends(get_session)) -> FormularioRepository:
    return FormularioRepository(session=session)

def get_usuario_repository(session: Session = Depends(get_session)) -> UsuarioRepository:
    return UsuarioRepository(session=session)

def get_questao_repository(session: Session = Depends(get_session)) -> QuestaoRepository:
    return QuestaoRepository(session=session)

def get_alternativa_repository(session: Session = Depends(get_session)) -> AlternativaRepository:
    return AlternativaRepository(session=session)

def get_resposta_repository(session: Session = Depends(get_session)) -> RespostaRepository:
    return RespostaRepository(session=session)