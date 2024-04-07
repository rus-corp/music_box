from fastapi.responses import JSONResponse
from fastapi import status


access_denied_error = JSONResponse(content='access denied', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
not_Found_error = JSONResponse(content='Data not found', status_code=status.HTTP_404_NOT_FOUND)