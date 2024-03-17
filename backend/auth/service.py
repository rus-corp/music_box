from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], depraceted='auto')


class Hasher:
  @staticmethod
  def verify_password(plain_password, hashed_password):
    pass