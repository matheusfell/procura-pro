from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from app.database import get_db
from app.auth import get_password_hash, verificar_senha, verifica_token, criar_token_acesso
from app.schemas import UsuarioCriar, UsuarioLogado, UsuarioLogin, ServicoCriado, Avaliacao
import os
from datetime import timedelta

router = APIRouter()

# Diretório onde as imagens serão salvas
UPLOAD_FOLDER = "assets/img/img_banco"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.post("/ws/registrar", response_model=UsuarioLogado)
async def registrar(user: UsuarioCriar, db=Depends(get_db)):
    cursor = db.cursor()

    # Verificar se o email já está cadastrado
    cursor.execute("SELECT usuario_id FROM usuario WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Gerar o hash da senha
    senha_hash = get_password_hash(user.senha)

    # Inserir novo usuário no banco de dados
    cursor.execute(
        "INSERT INTO usuario(nome, senha, telefone, email, cpf, cidade, uf, rua, numero_casa) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING usuario_id",
        (user.nome, senha_hash, user.telefone, user.email, user.cpf, user.cidade, user.uf, user.rua, user.numero)
    )
    
    usuario_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()

    # Retorna os dados do usuário logado conforme esperado pelo modelo `UsuarioLogado`
    return UsuarioLogado(
        usuario_id=usuario_id,
        nome=user.nome,
        email=user.email,
        cidade=user.cidade,
        uf=user.uf
    )

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
        "imagem": caminho_imagem
    }

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServicos")
async def listar_servicos(nome: str = None, cidade: str = None, db=Depends(get_db)):
    cursor = db.cursor()

    # Construção da query com LEFT JOIN para evitar problemas com NULL nas avaliações
    query = """
    SELECT s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf, 
           u.nome, u.telefone, u.email, s.imagem, 
           ROUND(AVG(a.nota)) as nota 
    FROM servico s 
    JOIN usuario u ON s.usuario_id = u.usuario_id 
    LEFT JOIN avaliacao_servico a ON s.servico_id = a.servico_id 
    """

    # Condições dinâmicas
    conditions = []
    params = []

    if nome:
        conditions.append("s.descricao ILIKE %s")
        params.append(f"%{nome}%")
        
    if cidade:
        conditions.append("s.cidade ILIKE %s")
        params.append(f"%{cidade}%")
    
    # Adiciona as condições na query caso existam
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Agrupamento final
    query += " GROUP BY s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf, u.nome, u.telefone, u.email, s.imagem"

    # Executa a query com os parâmetros
    cursor.execute(query, tuple(params))
    servicos = cursor.fetchall()
    cursor.close()

    # Processa o resultado
    servicos_list = []
    for servico in servicos:
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
            "nota": servico[10] or 0,  # Caso nota seja None, define como 0
            "imagem": imagem_path
        }
        servicos_list.append(servico_dict)

    return {"servicos": servicos_list}


#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

@router.get("/ws/buscarServico/{servico_id}")
async def obter_servico(servico_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    # Consulta ajustada para incluir a média da nota e a quantidade de avaliações
    cursor.execute("""
        SELECT s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf, 
               u.nome, u.telefone, u.email, s.imagem, 
               ROUND(AVG(a.nota)) as nota, COUNT(a.servico_id) as quantidadeAvaliacoes
        FROM servico s
        JOIN usuario u ON s.usuario_id = u.usuario_id
        LEFT JOIN avaliacao_servico a ON s.servico_id = a.servico_id
        WHERE s.servico_id = %s
        GROUP BY s.servico_id, s.descricao, s.valor, s.usuario_id, s.cidade, s.uf, 
                 u.nome, u.telefone, u.email, s.imagem
    """, (servico_id,))
    servico = cursor.fetchone()
    cursor.close()

    # Processa o resultado da consulta
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
            "nota": servico[10] or 0,  # Média da nota
            "quantidadeAvaliacoes": servico[11] or 0,  # Quantidade de avaliações
            "imagem": imagem_path
        }
        return servico_dict
    else:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------#


# Rota para inserir uma nova avaliação
@router.post("/ws/avaliarServico", response_model=Avaliacao)
async def inserir_avaliacao(avaliacao: Avaliacao, db = Depends(get_db)):
    cursor = db.cursor()
    
    # Validação da nota
    if avaliacao.nota < 1 or avaliacao.nota > 5:
        raise HTTPException(status_code=400, detail="A nota deve estar entre 1 e 5.")
    
    # Inserção da avaliação
    cursor.execute("""
        INSERT INTO avaliacao_servico (servico_id,  usuario_id , nota) 
        VALUES (%s, %s, %s)
    """, (avaliacao.servico_id, avaliacao.usuario_id, avaliacao.nota))
    db.commit()
    cursor.close()
    
    return avaliacao


UPLOAD_FOLDER = "assets/img/img_banco"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------#

# Rota para listar serviços do usuário logado com opções de edição e exclusão
@router.get("/ws/meusServicos/{usuario_id}")
async def listar_meus_servicos(usuario_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT servico_id, descricao, valor, cidade, uf, imagem
        FROM servico
        WHERE usuario_id = %s
    """, (usuario_id,))
    servicos = cursor.fetchall()
    cursor.close()

    servicos_list = []
    for servico in servicos:
        servicos_list.append({
            "servico_id": servico[0],
            "descricao": servico[1],
            "valor": servico[2],
            "cidade": servico[3],
            "uf": servico[4],
            "imagem": f"http://localhost:8000{servico[5]}" if servico[5] else "/assets/img/default.png"
        })

    return {"servicos": servicos_list}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------#

# Rota para editar um serviço
@router.put("/ws/editarServico/{servico_id}")
async def editar_servico(servico_id: int, descricao: str = Form(...), valor: float = Form(...), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE servico
        SET descricao = %s, valor = %s
        WHERE servico_id = %s
    """, (descricao, valor, servico_id))
    db.commit()
    cursor.close()

    return {"message": "Serviço atualizado com sucesso"}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------#

# Rota para excluir um serviço
@router.delete("/ws/excluirServico/{servico_id}")
async def excluir_servico(servico_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM servico WHERE servico_id = %s", (servico_id,))
    db.commit()
    cursor.close()

    return {"message": "Serviço excluído com sucesso"}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------#

