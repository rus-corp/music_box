import uvicorn


from backend.main_app import app




if __name__ == '__main__':
  uvicorn.run(app)