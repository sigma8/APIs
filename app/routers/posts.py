from typing import  List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )

#obtener todos los posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db),
            get_current_user: int = Depends(oauth2.get_current_user), 
            limit: int = 10, skip: int = 0):
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    return posts

#crear un post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(database.get_db),
                get_current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#obtener un post por id
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(database.get_db),
            get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post {id} no fue encontrado")
    return post

#borrar un post por id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db),
                get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post {id} no fue encontrado")
    if post.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="No esta autorizado para realizar esta accion")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#actualizar un post, todo el post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(database.get_db),
                get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_update = post_query.first()
    if post_update == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post {id} no fue encontrado")
    if post_update.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="No esta autorizado para realizar esta accion")
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    return post_query.first()