from fastapi.responses import JSONResponse
from fastapi import status


access_denied_error = JSONResponse(content='access denied',
                                   status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
not_Found_error = JSONResponse(content='Data not found',
                               status_code=status.HTTP_404_NOT_FOUND)

not_parameters = JSONResponse(content='Не переданы необходимые параметры',
                              status_code=400)



def found_error_in_db(data, id):
  JSONResponse(content=f'{data} with {id} not found',
               status_code=status.HTTP_404_NOT_FOUND)
  




def relation_exist(user_id: int, client_group_id: int, status: bool = True):
  if not status:
    return JSONResponse(content=f'User with id {user_id} has not in group {client_group_id}', 
                        status_code=400)
  else:
    return JSONResponse(content=f'User with id {user_id} has in group {client_group_id}',
                        status_code=400)