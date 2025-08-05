from models import UsuarioModel
from repositories import UsuarioRepository
from schemas import UsuarioCreate, UsuarioRead, UsuarioUpdate
from dependencies import get_usuario_repository
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

router = APIRouter()
@router.get("/usuarios", response_model=list[UsuarioRead])
def read_usuarios(
    skip: int = 0,
    limit: int = 100,
    repository: UsuarioRepository = Depends(get_usuario_repository)
):
    usuarios = repository.get_all(skip=skip, limit=limit)
    return [UsuarioRead.from_usuario_model(u) for u in usuarios]

@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def read_usuario(
    usuario_id: int,
    repository: UsuarioRepository = Depends(get_usuario_repository)
):
    usuario = repository.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return UsuarioRead.from_usuario_model(usuario)

@router.post("/usuarios", response_model=UsuarioRead)
def create_usuario(
    usuario: UsuarioCreate,
    repository: UsuarioRepository = Depends(get_usuario_repository)
):
    now = datetime.now()
    usuario_model = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        ativo=usuario.ativo,
        data_criacao=now,
        data_modificacao=now
    )

    created_usuario = repository.create(usuario_model)
    return UsuarioRead.from_usuario_model(created_usuario)
