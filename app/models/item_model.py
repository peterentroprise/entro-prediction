from pydantic import BaseModel

class Item(BaseModel):
    context: str
    question: str