




class Permissions:
  def __init__(self, target_user=None, current_user=None) -> None:
    self.target_user = target_user
    self.current_user = current_user


  async def superuser_permission(self):
    if self.current_user.is_superuser == True:
      return True
    return False


async def manager_permission(self):pass


async def client_permission(self): pass


async def redactor_permission(self): pass


async def chek_user_permissions(): pass