from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(pwd: str, hash_pwd: str) -> bool:
    return CRIPTO.verify(pwd, hash_pwd)


def get_hash_pwd(pwd: str)-> str:
    return CRIPTO.hash(pwd)