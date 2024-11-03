from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from app.database import get_db
from app.auth import get_password_hash, verificar_senha, verifica_token, criar_token_acesso
from app.schemas import UsuarioCriar, UsuarioLogado, UsuarioLogin, ServicoCriado
import os
from datetime import timedelta

router = APIRouter()

# Diretório onde as imagens serão salvas
UPLOAD_FOLDER = "assets/img/img_banco"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.post("/ws/registrar", response_model=UsuarioLogado)
async def registar(user: UsuarioCriar, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT usuario_id from usuario where email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    senha_hash = get_password_hash(user.senha)

    cursor.execute(
        "INSERT INTO usuario(nome, senha, telefone, email, cpf, cidade, uf, rua, numero_casa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING usuario_id",
        (user.nome, senha_hash, user.telefone, user.email, user.cpf, user.cidade, user.uf, user.rua, user.numero)
    )
    
    usuarioID = cursor.fetchone()[0]
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

    if not db_user or not verificar_senha(user.senha, db_user[1]):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    usuarioId = int(db_user[0])
    nome = str(db_user[2])
    cidade = str(db_user[3])
    uf = str(db_user[4])

    # Criar o token de acesso
    access_token_expires = timedelta(minutes=30)
    access_token = criar_token_acesso(
        data={"sub": str(db_user[0])}, expires_delta=access_token_expires
    )

    return {"idUsuario": usuarioId, "nome": nome, "cidade": cidade, "uf": uf, "access_token": access_token, "token_type": "bearer"}

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.post("/ws/registrarServico", response_model=ServicoCriado)
async def registar_servico(
    descricao: str = Form(...),
    valor: float = Form(...),
    usuario_id: int = Form(...),
    cidade: str = Form(...),
    uf: str = Form(...),
    imagem: UploadFile = File(...),  # Parâmetro para o upload de imagem
    db=Depends(get_db)
):
    cursor = db.cursor()

    # Verifica se já existe um serviço semelhante para o usuário
    cursor.execute("SELECT servico_id FROM servico WHERE descricao = %s AND usuario_id = %s", 
                   (descricao, usuario_id))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Serviço semelhante já cadastrado")

    # Salva a imagem no sistema de arquivos
    filename = f"{usuario_id}_{imagem.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(await imagem.read())
    
    # Certifique-se de que caminho_imagem é uma string com o caminho relativo
    caminho_imagem = f"/assets/img/img_banco/{filename}"

    # Insere o serviço e o caminho da imagem no banco de dados
    cursor.execute(
        "INSERT INTO servico(descricao, valor, usuario_id, cidade, uf, imagem) VALUES (%s, %s, %s, %s, %s, %s) RETURNING servico_id",
        (descricao, valor, usuario_id, cidade, uf, caminho_imagem)
    )
    
    servicoID = cursor.fetchone()[0]
    db.commit()
    cursor.close()

    return {
        "servico_id": servicoID, 
        "descricao": descricao, 
        "valor": valor, 
        "usuario_id": usuario_id, 
        "cidade": cidade, 
        "uf": uf, 
        "imagem": caminho_imagem  # Confirme que este campo é uma string
    }

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServicos")
async def listar_servicos(nome: str = None, cidade: str = None, db=Depends(get_db)):
    cursor = db.cursor()

    # Iniciar a query base
    query = "SELECT s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf, u.nome, u.telefone, u.email, s.imagem FROM servico s JOIN usuario u ON s.usuario_id = u.usuario_id"
    
    # Lista de condições para o WHERE
    conditions = []
    
    # Adicionar condições com base nos parâmetros de filtro
    if nome:
        conditions.append("s.descricao ILIKE %s")
    if cidade:
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

    # Transformar os resultados em uma lista de dicionários com URL completa da imagem
    servicos_list = []
    for servico in servicos:
        # Certifique-se de que imagem_path é uma string, e não uma referência de memória
        imagem_path = f"http://localhost:8000{servico[9]}" if servico[9] else "/assets/img/default.png"
        
        servico_dict = {
            "id": servico[0],
            "descricao": servico[1],
            "valor": servico[2],
            "usuario_id": servico[3],
            "cidade": servico[4],
            "uf": servico[5],
            "usuario_nome": servico[6],
            "usuario_telefone": servico[7],
            "usuario_email": servico[8],
            "imagem": imagem_path  # Verifique que está sendo passada corretamente como string
        }
        servicos_list.append(servico_dict)

    return {"servicos": servicos_list}

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServico/{servico_id}")
async def obter_servico(servico_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""
        SELECT s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf, u.nome, u.telefone, u.email, s.imagem
        FROM servico s
        JOIN usuario u ON s.usuario_id = u.usuario_id
        WHERE s.servico_id = %s
    """, (servico_id,))
    servico = cursor.fetchone()
    cursor.close()

    if servico:
        imagem_path = f"http://localhost:8000{servico[9]}" if servico[9] else "/assets/img/default.png"
        
        servico_dict = {
            "id": servico[0], 
            "descricao": servico[1], 
            "valor": servico[2], 
            "usuario_id": servico[3],
            "cidade": servico[4], 
            "uf": servico[5],
            "usuario_nome": servico[6],
            "usuario_telefone": servico[7],
            "usuario_email": servico[8],
            "imagem": imagem_path
        }
        return servico_dict
    else:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
