from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verificar_senha(senha, hash_senha):
    return pwd_context.verify(senha, hash_senha)