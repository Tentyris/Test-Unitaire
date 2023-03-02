from pydantic import BaseModel


class Item(BaseModel):
    task: str
    rating:int


class ItemCreate:
    def dict(self):
        pass
