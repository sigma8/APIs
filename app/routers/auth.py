from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .. import models, schemas, utils, database, oauth2

router = APIRouter(
    tags=["Authentication"]
    )

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
        db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Credenciales invalidas")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Credenciales invalidas")
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "user_email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
