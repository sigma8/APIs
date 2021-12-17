from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.utils import password_hash
from . import models, database
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()



#Conectar a la base de datos 
while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastAPi', 
                                user='postgres', 
                                password='1234', 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Se ha conectado exitosamente a la base de datos")
        break
    except Exception as error:
        print("Error al intentar conectarse a la base de datos")
        print("Error: ", error)
        time.sleep(3)

 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "bienvenido a mi api"}



