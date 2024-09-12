from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.auth import get_password_hash, verificar_senha, verifica_token, criar_token_acesso 
from app.schemas import UsuarioCriar, UsuarioLogado, UsuarioLogin
import psycopg2
from datetime import timedelta

router = APIRouter()

@router.post("/ws/registrar", response_model=UsuarioLogado)
async def registar(user: UsuarioCriar, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT usuario_id from usuario where email = %s",(user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code = 400, detail="Email já cadastrado")
    
    senha_hash = get_password_hash(user.senha)

    cursor.execute(
        "INSERT INTO usuario(nome, senha, idade, email, cpf, cidade_id, rua, complemento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING usuario_id",
        (user.nome, senha_hash, user.idade, user.email, user.cpf, user.cidade_id, user.rua, user.complemento)
    )
    
    usuarioID = cursor.fetchone()[0]
    print(usuarioID)
    db.commit()
    cursor.close()

    return {"usuario_id": usuarioID, "email": user.email}

@router.post("/ws/login")
async def login(user: UsuarioLogin, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT usuario_id, senha FROM usuario where email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()

    if not db_user or not verificar_senha(user.senha, db_user[1]):
        raise HTTPException(status_code = 400, detail = "Credenciais invalidas")
    
    # Criar o token de acesso
    access_token_expires = timedelta(minutes=30)
    access_token = criar_token_acesso(
        data={"sub": str(db_user[0])}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
