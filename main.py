from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from controllers import FormularioController, UsuarioController, QuestaoController, AlternativaController, RespostaController
from config import create_db_and_tables, drop_db_and_tables
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    #drop_db_and_tables()  # Dropar tabelas se necessário
    create_db_and_tables()
    yield 
    
    
app = FastAPI(title="API para gestão de faltas", version="0.0.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(FormularioController.router, prefix="/api/v1", tags=["formularios"])
app.include_router(UsuarioController.router, prefix="/api/v1", tags=["usuarios"])
app.include_router(QuestaoController.router, prefix="/api/v1", tags=["questoes"])
app.include_router(AlternativaController.router, prefix="/api/v1", tags=["alternativas"])
app.include_router(RespostaController.router, prefix="/api/v1", tags=["respostas"])

if __name__ == "__main__":
    import uvicorn
    print("Iniciando o servidor FastAPI...")
    uvicorn.run(app, host="localhost", port=8000)