from models import FormularioModel
from repositories import FormularioRepository
from schemas import FormularioRead, FormularioCreate, FormularioUpdate
from dependencies import get_formulario_repository
from fastapi import APIRouter, Depends
from datetime import datetime

router = APIRouter()
@router.get("/formularios", response_model=list[FormularioRead])
def read_formularios(
    skip: int = 0,
    limit: int = 100,
    repository: FormularioRepository = Depends(get_formulario_repository)
):
    formularios = repository.get_all(skip=skip, limit=limit)
    return [FormularioRead.from_orm(f) for f in formularios]

@router.post("/formularios", response_model=FormularioRead)
def create_formulario(
    formulario: FormularioCreate,
    repository: FormularioRepository = Depends(get_formulario_repository)
):
    now = datetime.now()
    formulario_model = FormularioModel(
        titulo=formulario.titulo,
        descricao=formulario.descricao,
        ativo=formulario.ativo,
        data_criacao=now,
        data_modificacao=now
    )

    created_formulario = repository.create(formulario_model)
    return FormularioRead.from_orm(created_formulario)