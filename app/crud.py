
from sqlalchemy.orm import Session
from . import models, schemas


def get_courier(db: Session, courier_id: int):
    return db.query(models.Courier).filter(models.Courier.id == courier_id).first()

def get_couriers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Courier).offset(skip).limit(limit).all()

def create_courier(db: Session, courier: schemas.CourierCreate):
    db_courier = models.Courier(name=courier.name, districts=courier.districts)
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate, courier_id: int):
    db_order = models.Order(**order.dict(), courier_id=courier_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Устанавливаем active_order курьера в order_id
    db_courier = get_courier(db, courier_id)
    db_courier.active_order = db_order.id
    db.commit()
    db.refresh(db_courier)
    
    return db_order

def complete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db_order.status = 2
    db.commit()
    db.refresh(db_order)
    return db_order

def get_courier_by_name(db: Session, name: str):
    return db.query(models.Courier).filter(models.Courier.name == name).first()

def get_available_courier(db: Session, district: str):
    # Проверяем, что active_order у курьера равен None и что район курьера соответствует заданному в запросе
    return db.query(models.Courier).filter(
        models.Courier.districts.contains([district]),
        models.Courier.active_order.is_(None)
    ).first()