from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
import time
from . import models
from .database import engine, get_db



models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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


my_posts = [{"title": "mi primer post", "content": "contenido de mi primer post", "id": 1}, 
{"title": "cosas que amo", "content": "volar y escalar", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "bienvenido a mi api"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #posts =  cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) 
    #                RETURNING * """,
    #                (post.title, post.content, post.published)
    #                )
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post {id} no fue encontrado")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post {id} no fue encontrado"}
    return {"post details": post}


#@app.get("/sqlalchemy")
#def test_post(db: Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
#    return {"data": posts}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    #delete_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post {id} no fue encontrado")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
    #                WHERE id = %s
    #                RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_update = post_query.first()
    if post_update == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post {id} no fue encontrado")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}