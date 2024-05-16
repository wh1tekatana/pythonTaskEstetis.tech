from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/courier/", response_model=schemas.Courier)
def create_courier(courier: schemas.CourierCreate, db: Session = Depends(get_db)):
    db_courier = crud.get_courier_by_name(db, name=courier.name)
    if db_courier:
        raise HTTPException(status_code=400, detail="Данный курьер уже зарегистрирован")
    return crud.create_courier(db=db, courier=courier)

@app.get("/courier/", response_model=List[schemas.Courier])
def read_couriers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    couriers = crud.get_couriers(db, skip=skip, limit=limit)
    return couriers

@app.get("/courier/{courier_id}", response_model=schemas.Courier)
def read_courier(courier_id: int, db: Session = Depends(get_db)):
    db_courier = crud.get_courier(db, courier_id=courier_id)
    if db_courier is None:
        raise HTTPException(status_code=404, detail="Курьер не найден")
    return db_courier

@app.post("/order/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_courier = crud.get_available_courier(db, order.district)
    if db_courier is None:
        raise HTTPException(status_code=404, detail="Нет доступного курьера")
    return crud.create_order(db=db, order=order, courier_id=db_courier.id)

@app.get("/order/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return db_order

@app.post("/order/{order_id}", response_model=schemas.Order)
def complete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if db_order.status == 2:
        raise HTTPException(status_code=400, detail="Заказ уже завершен")
    return crud.complete_order(db=db, order_id=order_id)