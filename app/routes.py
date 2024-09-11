from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.auth import get_password_hash, verificar_senha
from app.schemas import UsuarioCriar, UsuarioLogado, UsuarioLogin
import psycopg2

router = APIRouter()

@router.post("/ws/registrar", response_model=UsuarioLogado)
async def registar(user: UsuarioCriar, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT usuarioID from usuario email =%s",(user.email))
    if cursor.fetchone():
        raise HTTPException(status_code = 400, detail="Email já cadastrado")
    
    senha_hash = get_password_hash(user.senha)

    cursor.execute(
        "INSERT INTO usuario(nome, senha, idade, email, cpf, cidadeID, rua, complemento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING usuarioID",
        (user.nome, user.senha, user.idade, user.email, user.cpf, user.cidade_id, user.rua, user.complemento)
    )
    
    usuarioID = cursor.fetchone()[0]
    db.commit()
    cursor.close()

    return {"ID": usuarioID, "email": user.email}

@router.post("/ws/login")
async def login(user: UsuarioLogin, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT usuarioID, senha FROM usuario where email = %s", (user.email))
    db_user = cursor.fetchone()
    cursor.close()

    if not db_user or not verificar_senha(user.senha, db_user[1]):
        raise HTTPException(status_code = 400, detail = "Credenciais invalidas")
    
    return {"message": "Login Bem-Sucedido", "usuarioID": db_user[0]}
