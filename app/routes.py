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

    cursor.execute("SELECT usuario_id, senha, nome, cidade, uf FROM usuario where email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()

    usuarioId = int(db_user[0])
    nome = str(db_user[2])
    cidade = str(db_user[3])
    uf = str(db_user[4])

    if not db_user or not verificar_senha(user.senha, db_user[1]):
        raise HTTPException(status_code = 400, detail = "Credenciais invalidas")
    
    # Criar o token de acesso
    access_token_expires = timedelta(minutes=30)
    access_token = criar_token_acesso(
        data={"sub": str(db_user[0])}, expires_delta=access_token_expires
    )

    return {"idUsuario": usuarioId, "nome": nome, "cidade": cidade, "uf": uf, "access_token": access_token, "token_type": "bearer"}

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.post("/ws/registrarServico", response_model=ServicoCriado)
async def registar(servico: ServicoCriar, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT servico_id from servico where descricao = %s and usuario_id = %s",(servico.descricao, servico.usuario_id))
    if cursor.fetchone():
        raise HTTPException(status_code = 400, detail="serviço semelhante já cadastrado")

    cursor.execute(
        "INSERT INTO servico(descricao, valor, usuario_id, cidade, uf) VALUES (%s, %s, %s, %s, %s) RETURNING servico_id",
        (servico.descricao, servico.valor, servico.usuario_id, servico.cidade, servico.uf)
    )
    
    servicoID = cursor.fetchone()[0]
    db.commit()
    cursor.close()

    return {"servico_id": servicoID, "descricao": servico.descricao, "valor": servico.valor, "usuario_id": servico.usuario_id, "cidade": servico.cidade, "uf": servico.uf}

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServicos")
async def listar_servicos(nome: str = None, cidade: str = None, db=Depends(get_db)):
    cursor = db.cursor()

    # Iniciar a query base
    query = "SELECT s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf  FROM servico s"
    
    # Lista de condições para o WHERE
    conditions = []
    
    # Adicionar condições com base nos parâmetros de filtro
    if nome:
        conditions.append("s.descricao ILIKE %s")
    if cidade:
        query += " JOIN usuario c ON s.usuario_id = c.usuario_id"
        conditions.append("s.cidade ILIKE %s")
    
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
    servicos_list = [{"id": servico[0], 
                      "nome": servico[1], 
                      "descricao": servico[2], 
                      "usuario_id": servico[3], 
                      "cidade": servico[4], 
                      "uf": servico[5]} for servico in servicos]

    return {"servicos": servicos_list}

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServico/{servico_id}")
async def obter_servico(servico_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""
        SELECT s.servico_id, s.descricao, s.valor, s.usuario_id, u.cidade, u.uf
        FROM servico s
        JOIN usuario u ON s.usuario_id = u.usuario_id
        WHERE s.servico_id = %s
    """, (servico_id,))
    servico = cursor.fetchone()
    cursor.close()

    if servico:
        servico_dict = {"id": servico[0], 
                      "nome": servico[1], 
                      "descricao": servico[2], 
                      "usuario_id": servico[3], 
                      "cidade": servico[4], 
                      "uf": servico[5] }
        return servico_dict
    else:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")