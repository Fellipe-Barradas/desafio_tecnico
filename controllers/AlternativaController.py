from repositories import AlternativaRepository
from schemas import AlternativaCreate, AlternativaRead, AlternativaUpdate
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_alternativa_repository
from models import AlternativaModel

router = APIRouter()

@router.get("/alternativas", response_model=list[AlternativaRead])
def read_alternativas(
    questao_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    somente_ativos: bool = True,
    alternativa_repo: AlternativaRepository = Depends(get_alternativa_repository)
):
    alternativas = alternativa_repo.get_all(
        skip=skip,
        limit=limit,
        somente_ativos=somente_ativos,
        questao_id=questao_id
    )
    return [AlternativaRead.from_model(a) for a in alternativas]

@router.get("/questoes/{questao_id}/alternativas", response_model=list[AlternativaRead])
def read_alternativas_by_questao(
    questao_id: int,
    somente_ativos: bool = True,
    alternativa_repo: AlternativaRepository = Depends(get_alternativa_repository)
):
    alternativas = alternativa_repo.get_by_questao_id(
        questao_id=questao_id,
        somente_ativos=somente_ativos
    )
    return [AlternativaRead.from_model(a) for a in alternativas]

@router.get("/alternativas/{alternativa_id}", response_model=AlternativaRead)
def read_alternativa(
    alternativa_id: int,
    alternativa_repo: AlternativaRepository = Depends(get_alternativa_repository)
):
    alternativa = alternativa_repo.get_by_id(alternativa_id)
    if not alternativa:
        raise HTTPException(status_code=404, detail="Alternativa não encontrada")
    return AlternativaRead.from_model(alternativa)

@router.post("/alternativas", response_model=AlternativaRead)
def create_alternativa(
    alternativa: AlternativaCreate,
    alternativa_repo: AlternativaRepository = Depends(get_alternativa_repository)
):
    alternativa_model = AlternativaModel(
        texto=alternativa.texto,
        correta=alternativa.correta,
        ativo=alternativa.ativo,
        questao_id=alternativa.questao_id
    )
    created_alternativa = alternativa_repo.create(alternativa_model)
    return AlternativaRead.from_model(created_alternativa)

@router.put("/alternativas/{alternativa_id}", response_model=AlternativaRead)
def update_alternativa(
    alternativa_id: int,
    alternativa: AlternativaUpdate,
    alternativa_repo: AlternativaRepository = Depends(get_alternativa_repository)
):
    existing_alternativa = alternativa_repo.get_by_id(alternativa_id)
    if not existing_alternativa:
        raise HTTPException(status_code=404, detail="Alternativa não encontrada")

    existing_alternativa.texto = alternativa.texto if alternativa.texto is not None else existing_alternativa.texto
    existing_alternativa.correta = alternativa.correta if alternativa.correta is not None else existing_alternativa.correta
    existing_alternativa.ativo = alternativa.ativo if alternativa.ativo is not None else existing_alternativa.ativo
    
    updated_alternativa = alternativa_repo.update(existing_alternativa)
    return AlternativaRead.from_model(updated_alternativa)

@router.delete("/alternativas/{alternativa_id}", response_model=dict)
def delete_alternativa(
    alternativa_id: int,
    alternativa_repo: AlternativaRepository = Depends(get_alternativa_repository)
):
    try:
        alternativa_repo.delete(alternativa_id)
        return {"detail": "Alternativa deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
