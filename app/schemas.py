from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: str
    cpf: str
    cidade: str
    uf: str
    rua: str
    numero: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioLogado(BaseModel):
    email: EmailStr
    usuario_id: int
    nome: str
    cidade: str
    uf: str
    
class ServicoCriar(BaseModel):
    descricao: str
    valor: float
    usuario_id: int
    cidade: str
    uf: str

class ServicoCriado(BaseModel):
    servico_id: int
    descricao: str
    valor: float
    cidade: str
    uf: str
    usuario_id: int