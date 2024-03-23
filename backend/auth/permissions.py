




class Permissions:
  def __init__(self, target_user=None, current_user=None) -> None:
    self.target_user = target_user
    self.current_user = current_user


  @staticmethod
  async def has_role_permission(current_user):
    if current_user.is_superuser == True:
      return True
    return False
    


async def chek_user_permissions(): pass