from fastapi import Depends
from sqlmodel import Session
from config import get_session
from repositories import FormularioRepository, UsuarioRepository

def get_formulario_repository(session: Session = Depends(get_session)) -> FormularioRepository:
    return FormularioRepository(session=session)

def get_usuario_repository(session: Session = Depends(get_session)) -> UsuarioRepository:
    return UsuarioRepository(session=session)