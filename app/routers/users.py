from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from .. import models, schemas, utils, database


router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResp)
def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db)):
    passhash = utils.password_hash(user.password)
    user.password = passhash
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResp)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user {id} no fue encontrado")
    return user
