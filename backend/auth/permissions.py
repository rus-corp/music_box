import os
from dotenv import load_dotenv

load_dotenv()

m_role = os.getenv('M_ROLE')
r_role = os.getenv('R_ROLE')
c_role = os.getenv('C_ROLE')
from backend.users.models import User



class Permissions:
  def __init__(self, current_user: User=None) -> None:
    self.current_user = current_user


  def superuser_permission(self):
    if self.current_user.is_superuser:
      return True
    return False


  def manager_permission(self):
    if self.current_user.role.role_name == m_role or self.current_user.is_superuser == True:
      return True
    return False


  def redactor_permission(self):
    if self.current_user.role.role_name == r_role or self.current_user.is_superuser == True:
      return True
    return False


  def client_permission(self):
    if self.current_user.role.role_name == c_role and self.current_user.is_superuser == True:
      return True
    return False


  async def chek_user_permissions(): pass