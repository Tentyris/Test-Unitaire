from fastapi import FastAPI, Body, Depends
import schemas
import Model

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()


@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(Model.Item).all()
    return items


@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item = session.query(Model.Item).get(id)
    return item


@app.post("/")
def addItem(item: schemas.Item, session: Session = Depends(get_session)):
    item = Model.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.put("/{id}")
def updateItem(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(Model.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    itemObject = session.query(Model.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'item terminated '
