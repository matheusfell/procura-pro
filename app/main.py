from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuração para servir arquivos estáticos
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Incluir o roteador das rotas da aplicação
app.include_router(router)

# Configuração do middleware CORS para permitir requisições de origens diferentes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)
