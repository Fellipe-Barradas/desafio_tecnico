from sqlmodel import Session, select, Sequence
from typing import Sequence
from models import FormularioModel

class FormularioRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100, somente_ativos: bool = True) -> Sequence[FormularioModel]:
        query = select(FormularioModel).offset(skip).limit(limit)
        if somente_ativos:
            query = query.where(FormularioModel.ativo == True)
        formularios: Sequence[FormularioModel] = self.session.exec(query).all()
        return formularios
    
    def get_by_id(self, formulario_id: int) -> FormularioModel | None:
        query = select(FormularioModel).where(FormularioModel.id == formulario_id)
        return self.session.exec(query).one_or_none()
    
    def create(self, formulario: FormularioModel) -> FormularioModel:
        self.session.add(formulario)
        self.session.commit()
        self.session.refresh(formulario)
        return formulario
    
    def update(self, formulario: FormularioModel) -> FormularioModel:
        self.session.add(formulario)
        self.session.commit()
        self.session.refresh(formulario)
        return formulario
    
    def delete(self, formulario_id: int) -> None:
        formulario = self.get_by_id(formulario_id)
        if formulario:
            self.session.delete(formulario)
            self.session.commit()
        else:
            raise ValueError("Formulario not found")