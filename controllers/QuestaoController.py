from repositories import QuestaoRepository
from schemas import QuestaoCreate, QuestaoRead, QuestaoUpdate
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_questao_repository
from datetime import datetime
from models import QuestaoModel

router = APIRouter()
@router.get("/questoes", response_model=list[QuestaoRead])
def read_questoes(
    formulario_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    somente_ativos: bool = True,
    questao_repo: QuestaoRepository = Depends(get_questao_repository)
):
    questoes = questao_repo.get_all(
        skip=skip,
        limit=limit,
        somente_ativos=somente_ativos,
        formulario_id=formulario_id
    )
    return [QuestaoRead.from_model(q) for q in questoes]

@router.get("/questoes/{questao_id}", response_model=QuestaoRead)
def read_questao(
    questao_id: int,
    questao_repo: QuestaoRepository = Depends(get_questao_repository)
):
    questao = questao_repo.get_by_id(questao_id)
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    return QuestaoRead.from_model(questao)

@router.post("/questoes", response_model=QuestaoRead)
def create_questao(
    questao: QuestaoCreate,
    questao_repo: QuestaoRepository = Depends(get_questao_repository)
):
    now = datetime.now()
    questao_model = QuestaoModel(
        enunciado=questao.enunciado,
        tipo=questao.tipo,
        ativo=questao.ativo,
        formulario_id=questao.formulario_id
    )
    questao_repo.create(questao_model)
    return QuestaoRead.from_model(questao_model)

@router.put("/questoes/{questao_id}", response_model=QuestaoRead)
def update_questao(
    questao_id: int,
    questao: QuestaoUpdate,
    questao_repo: QuestaoRepository = Depends(get_questao_repository)
):
    existing_questao = questao_repo.get_by_id(questao_id)
    if not existing_questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")

    existing_questao.enunciado = questao.enunciado if questao.enunciado is not None else existing_questao.enunciado
    existing_questao.tipo = questao.tipo if questao.tipo is not None else existing_questao.tipo
    existing_questao.ativo = questao.ativo if questao.ativo is not None else existing_questao.ativo
    questao_repo.update(existing_questao)
    return QuestaoRead.from_model(existing_questao)

@router.delete("/questoes/{questao_id}", response_model=dict)
def delete_questao(
    questao_id: int,
    questao_repo: QuestaoRepository = Depends(get_questao_repository)
):
    try:
        questao_repo.delete(questao_id)
        return {"detail": "Questão deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))