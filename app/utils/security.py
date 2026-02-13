from datetime import timedelta
import random
from datetime import datetime , timedelta
import string 
pws_context =CryptContext(Schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_contex.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

# verification code 

def genarate_verification_code():
    return ''.join(random.choices(string.digits,k=6))

def verification_expiry(minutes=10):
    return datetime.utcnow()+ timedelta(minutes=minutes)    