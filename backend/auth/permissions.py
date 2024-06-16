

from backend.users.models import User



class Permissions:
  def __init__(self, target_user: User=None, current_user: User=None) -> None:
    self.target_user = target_user
    self.current_user = current_user


  async def superuser_permission(self):
    if self.current_user.is_superuser:
      return True
    return False


  async def manager_permission(self):
    if self.current_user.role == 'manager' or self.current_user.is_superuser == True:
      return True
    return False


  async def redactor_permission(self):
    if self.current_user.role == 'redactor' or self.current_user.is_superuser == True:
      return True
    return False


  async def client_permission(self):
    if self.current_user.role == 'client' and self.current_user.is_superuser == True:
      return True
    return False


  async def chek_user_permissions(): pass