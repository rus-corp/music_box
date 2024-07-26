from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
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

origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://64.226.111.161",
    "http://64.226.111.161:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
  return {'mes': 'hello from'}







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


