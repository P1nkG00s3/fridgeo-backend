from sqlalchemy.orm import Session

from models import models

def get_products(db: Session, skip: int = 0, limit: int= 100):
    return db.query(models.ListOfProducts).offset(skip).limit(limit).all()