from fastapi import Depends
from sqlmodel import Session
from config import get_session
from repositories import FormularioRepository

def get_formulario_repository(session: Session = Depends(get_session)) -> FormularioRepository:
    return FormularioRepository(session=session)