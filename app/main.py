from fastapi import FastAPI
from app.utils import password_hash
from . import models, database
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "bienvenido a mi api"}



