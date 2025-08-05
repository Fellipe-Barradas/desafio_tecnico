from models import FormularioModel
from repositories import FormularioRepository
from schemas import FormularioRead, FormularioCreate, FormularioUpdate
from dependencies import get_formulario_repository
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

router = APIRouter()
@router.get("/formularios", response_model=list[FormularioRead])
def read_formularios(
    skip: int = 0,
    limit: int = 100,
    somente_ativos: bool = True,
    repository: FormularioRepository = Depends(get_formulario_repository)
):
    formularios = repository.get_all(skip=skip, limit=limit, somente_ativos=somente_ativos)
    return [FormularioRead.from_model(f) for f in formularios]

@router.get("/formularios/{formulario_id}", response_model=FormularioRead)
def read_formulario(
    formulario_id: int,
    repository: FormularioRepository = Depends(get_formulario_repository)
):
    formulario = repository.get_by_id(formulario_id)
    if not formulario:
        raise HTTPException(status_code=404, detail="Formulario not found")
    return FormularioRead.from_model(formulario)

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
        usuario_id=formulario.usuario_id,
        data_criacao=now,
        data_modificacao=now
    )

    created_formulario = repository.create(formulario_model)
    return FormularioRead.from_model(created_formulario)

@router.put("/formularios/{formulario_id}", response_model=FormularioRead)
def update_formulario(
    formulario_id: int,
    formulario: FormularioUpdate,
    repository: FormularioRepository = Depends(get_formulario_repository)
):
    existing_formulario = repository.get_by_id(formulario_id)
    if not existing_formulario:
        raise HTTPException(status_code=404, detail="Formulario not found")

    existing_formulario.titulo = formulario.titulo if formulario.titulo is not None else existing_formulario.titulo
    existing_formulario.descricao = formulario.descricao if formulario.descricao is not None else existing_formulario.descricao
    existing_formulario.ativo = formulario.ativo if formulario.ativo is not None else existing_formulario.ativo
    existing_formulario.data_modificacao = datetime.now()
    repository.update(existing_formulario)

    return FormularioRead.from_model(existing_formulario)

@router.delete("/formularios/{formulario_id}", response_model=dict)
def delete_formulario(
    formulario_id: int,
    repository: FormularioRepository = Depends(get_formulario_repository)
):
    try:
        repository.delete(formulario_id)
        return {"detail": "Formulario deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e