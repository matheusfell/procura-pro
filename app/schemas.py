from pydantic import BaseModel, EmailStr

class UsuarioCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    idade: int
    cpf: str
    cidade_id: int
    rua: str
    complemento: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioLogado(BaseModel):
    email: EmailStr
    usuario_id: int
    nome: str

