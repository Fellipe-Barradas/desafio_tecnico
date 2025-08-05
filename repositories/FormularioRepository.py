from sqlmodel import Session, select, Sequence
from models import FormularioModel

class FormularioRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[FormularioModel]:
        query = select(FormularioModel).offset(skip).limit(limit)
        formularios = self.session.exec(query).all()
        return formularios
    
    def create(self, formulario: FormularioModel) -> FormularioModel:
        self.session.add(formulario)
        self.session.commit()
        self.session.refresh(formulario)
        return formulario