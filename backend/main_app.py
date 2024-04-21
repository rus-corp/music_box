from fastapi import FastAPI, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
import os
from os import path



from .users.routers import router as users_routers
from .music.app_main_routers import router as music_routers
from .auth.routers import login_router
from .clients.main_router import router as client_router

from backend.database import get_db


app = FastAPI(
  title='Music Box'
)


@app.get("/")
async def root():
  return {'mes': 'hi'}




# media_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))

# if not os.path.exists(media_directory):
#     try:
#         os.makedirs(media_directory)
#         print("Directory 'media' created successfully.")
#     except Exception as e:
#         print(f"Error creating 'media' directory: {e}")


path_str = path.dirname(path.realpath(__file__))

app.mount('/media', StaticFiles(directory=f'{path_str}/media'), name='media')


app.include_router(users_routers)
app.include_router(music_routers)
app.include_router(login_router)
app.include_router(client_router)


