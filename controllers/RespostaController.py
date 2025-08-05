from repositories import RespostaRepository
from schemas import RespostaCreate, RespostaRead, RespostaUpdate
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_resposta_repository
from datetime import datetime
from models import RespostaModel

router = APIRouter()

@router.get("/respostas", response_model=list[RespostaRead])
def read_respostas(
    usuario_id: int | None = None,
    questao_id: int | None = None,
    alternativa_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    respostas = resposta_repo.get_all(
        skip=skip,
        limit=limit,
        usuario_id=usuario_id,
        questao_id=questao_id,
        alternativa_id=alternativa_id
    )
    return [RespostaRead.from_model(r) for r in respostas]

@router.get("/usuarios/{usuario_id}/respostas", response_model=list[RespostaRead])
def read_respostas_by_usuario(
    usuario_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    respostas = resposta_repo.get_by_usuario_id(usuario_id=usuario_id)
    return [RespostaRead.from_model(r) for r in respostas]

@router.get("/questoes/{questao_id}/respostas", response_model=list[RespostaRead])
def read_respostas_by_questao(
    questao_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    respostas = resposta_repo.get_by_questao_id(questao_id=questao_id)
    return [RespostaRead.from_model(r) for r in respostas]

@router.get("/alternativas/{alternativa_id}/respostas", response_model=list[RespostaRead])
def read_respostas_by_alternativa(
    alternativa_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    respostas = resposta_repo.get_by_alternativa_id(alternativa_id=alternativa_id)
    return [RespostaRead.from_model(r) for r in respostas]

@router.get("/respostas/{resposta_id}", response_model=RespostaRead)
def read_resposta(
    resposta_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    resposta = resposta_repo.get_by_id(resposta_id)
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return RespostaRead.from_model(resposta)

@router.get("/usuarios/{usuario_id}/questoes/{questao_id}/resposta", response_model=RespostaRead)
def read_resposta_by_usuario_and_questao(
    usuario_id: int,
    questao_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    resposta = resposta_repo.get_by_usuario_and_questao(usuario_id=usuario_id, questao_id=questao_id)
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return RespostaRead.from_model(resposta)

@router.post("/respostas", response_model=RespostaRead)
def create_resposta(
    resposta: RespostaCreate,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    # Verificar se já existe uma resposta para esta questão e usuário
    existing_resposta = resposta_repo.get_by_usuario_and_questao(
        usuario_id=resposta.usuario_id,
        questao_id=resposta.questao_id
    )
    
    if existing_resposta:
        raise HTTPException(
            status_code=400, 
            detail="Usuário já respondeu a esta questão"
        )
    
    # Validar que pelo menos um tipo de resposta foi fornecido
    if not resposta.valor and not resposta.alternativa_id:
        raise HTTPException(
            status_code=400,
            detail="Deve ser fornecido valor (para questão aberta) ou alternativa_id (para múltipla escolha)"
        )
    
    # Validar que não foram fornecidos ambos os tipos
    if resposta.valor and resposta.alternativa_id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível fornecer tanto valor quanto alternativa_id na mesma resposta"
        )
    
    now = datetime.now()
    resposta_model = RespostaModel(
        valor=resposta.valor,
        alternativa_id=resposta.alternativa_id,
        questao_id=resposta.questao_id,
        usuario_id=resposta.usuario_id,
        data_criacao=now,
        data_modificacao=now
    )
    created_resposta = resposta_repo.create(resposta_model)
    return RespostaRead.from_model(created_resposta)

@router.post("/questoes/{questao_id}/alternativas/{alternativa_id}/responder", response_model=RespostaRead)
def responder_multipla_escolha(
    questao_id: int,
    alternativa_id: int,
    usuario_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    """Endpoint específico para responder questões de múltipla escolha"""
    # Verificar se já existe uma resposta para esta questão e usuário
    existing_resposta = resposta_repo.get_by_usuario_and_questao(
        usuario_id=usuario_id,
        questao_id=questao_id
    )
    
    if existing_resposta:
        raise HTTPException(
            status_code=400, 
            detail="Usuário já respondeu a esta questão"
        )
    
    now = datetime.now()
    resposta_model = RespostaModel(
        valor=None,
        alternativa_id=alternativa_id,
        questao_id=questao_id,
        usuario_id=usuario_id,
        data_criacao=now,
        data_modificacao=now
    )
    created_resposta = resposta_repo.create(resposta_model)
    return RespostaRead.from_model(created_resposta)

@router.post("/questoes/{questao_id}/responder-texto", response_model=RespostaRead)
def responder_questao_aberta(
    questao_id: int,
    valor: str,
    usuario_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    """Endpoint específico para responder questões abertas"""
    # Verificar se já existe uma resposta para esta questão e usuário
    existing_resposta = resposta_repo.get_by_usuario_and_questao(
        usuario_id=usuario_id,
        questao_id=questao_id
    )
    
    if existing_resposta:
        raise HTTPException(
            status_code=400, 
            detail="Usuário já respondeu a esta questão"
        )
    
    now = datetime.now()
    resposta_model = RespostaModel(
        valor=valor,
        alternativa_id=None,
        questao_id=questao_id,
        usuario_id=usuario_id,
        data_criacao=now,
        data_modificacao=now
    )
    created_resposta = resposta_repo.create(resposta_model)
    return RespostaRead.from_model(created_resposta)

@router.put("/respostas/{resposta_id}", response_model=RespostaRead)
def update_resposta(
    resposta_id: int,
    resposta: RespostaUpdate,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    existing_resposta = resposta_repo.get_by_id(resposta_id)
    if not existing_resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")

    # Validar que não foram fornecidos ambos os tipos
    if resposta.valor and resposta.alternativa_id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível fornecer tanto valor quanto alternativa_id na mesma resposta"
        )

    # Atualizar apenas os campos fornecidos
    if resposta.valor is not None:
        existing_resposta.valor = resposta.valor
        existing_resposta.alternativa_id = None  # Limpar alternativa se fornecendo valor
    
    if resposta.alternativa_id is not None:
        existing_resposta.alternativa_id = resposta.alternativa_id
        existing_resposta.valor = None  # Limpar valor se fornecendo alternativa
    
    existing_resposta.data_modificacao = datetime.now()
    
    updated_resposta = resposta_repo.update(existing_resposta)
    return RespostaRead.from_model(updated_resposta)

@router.delete("/respostas/{resposta_id}", response_model=dict)
def delete_resposta(
    resposta_id: int,
    resposta_repo: RespostaRepository = Depends(get_resposta_repository)
):
    try:
        resposta_repo.delete(resposta_id)
        return {"detail": "Resposta deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
