from sqlmodel import Session, select, Sequence
from typing import Sequence
from models import UsuarioModel

class UsuarioRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[UsuarioModel]:
        query = select(UsuarioModel).offset(skip).limit(limit)
        usuarios: Sequence[UsuarioModel] = self.session.exec(query).all()
        return usuarios
    
    def get_by_id(self, usuario_id: int) -> UsuarioModel | None:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        return self.session.exec(query).one_or_none()

    def create(self, usuario: UsuarioModel) -> UsuarioModel:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario