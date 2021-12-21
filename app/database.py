from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#Conectar a la base de datos, para proposito educativo
#while True:
#    try:
#        conn = psycopg2.connect(host='localhost', 
#                                database='fastAPi', 
#                                user='postgres', 
#                                password='1234', 
#                                cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#       print("Se ha conectado exitosamente a la base de datos")
#        break
#    except Exception as error:
#        print("Error al intentar conectarse a la base de datos")
#        print("Error: ", error)
#        time.sleep(3)

