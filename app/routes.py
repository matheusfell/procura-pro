from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.auth import get_password_hash, verificar_senha, verifica_token, criar_token_acesso 
from app.schemas import UsuarioCriar, UsuarioLogado, UsuarioLogin, ServicoCriar, ServicoCriado
import psycopg2
from datetime import timedelta

router = APIRouter()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.post("/ws/registrar", response_model=UsuarioLogado)
async def registar(user: UsuarioCriar, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT usuario_id from usuario where email = %s",(user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code = 400, detail="Email já cadastrado")
    
    senha_hash = get_password_hash(user.senha)

    cursor.execute(
        "INSERT INTO usuario(nome, senha, telefone, email, cpf, cidade, uf, rua, numero_casa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING usuario_id",
        (user.nome, senha_hash, user.telefone, user.email, user.cpf, user.cidade, user.uf, user.rua, user.numero)
    )
    
    usuarioID = cursor.fetchone()[0]
    print(usuarioID)
    db.commit()
    cursor.close()

    return {"usuario_id": usuarioID, "nome": user.nome, "email": user.email}

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.post("/ws/registrarServico", response_model=ServicoCriado)
async def registar(servico: ServicoCriar, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT servico_id from servico where descricao = %s and usuario_id = %s",(servico.descricao, servico.usuario_id))
    if cursor.fetchone():
        raise HTTPException(status_code = 400, detail="serviço semelhante já cadastrado")

    cursor.execute(
        "INSERT INTO servico(descricao, valor, usuario_id) VALUES (%s, %s, %s) RETURNING servico_id",
        (servico.descricao, servico.valor, servico.usuario_id)
    )
    
    servicoID = cursor.fetchone()[0]
    db.commit()
    cursor.close()

    return {"servico_id": servicoID}

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServico")
async def listar_servicos(nome: str = None, cidade: str = None, db=Depends(get_db)):
    cursor = db.cursor()

    # Iniciar a query base
    query = "SELECT s.servico_id, s.descricao, s.valor, s.usuario_id  FROM servico s"
    
    # Lista de condições para o WHERE
    conditions = []
    
    # Adicionar condições com base nos parâmetros de filtro
    if nome:
        conditions.append("s.nome ILIKE %s")
    if cidade:
        query += " JOIN cidade c ON s.cidade_id = c.id"
        conditions.append("c.nome ILIKE %s")
    
    # Montar a query completa com as condições
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Preparar os parâmetros da query
    params = []
    if nome:
        params.append(f"%{nome}%")
    if cidade:
        params.append(f"%{cidade}%")
    
    # Executar a query
    cursor.execute(query, tuple(params))
    servicos = cursor.fetchall()
    cursor.close()

    # Transformar os resultados em uma lista de dicionários
    servicos_list = [{"id": servico[0], "nome": servico[1], "descricao": servico[2]} for servico in servicos]

    return {"servicos": servicos_list}