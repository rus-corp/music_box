import datetime
from datetime import timedelta, datetime
from jose import jwt


from config import SECRET_KEY, ALGORITHM



def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=30)
  to_encode.update({'exp': expire})
  enoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
  return enoded_jwt