from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/likes",
    tags = ["Likes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), 
        current_user: int = Depends(oauth2.get_current_user)):
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    print(found_like)
    if like.dir == True:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'Usuario {current_user.id} ya habia dicho que le gusta el post')
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Te gusta"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Like no existe')
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Like eliminado"}