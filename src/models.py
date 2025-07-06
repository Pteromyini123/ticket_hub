from pydantic import BaseModel
from typing import Optional

class Ticket(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    assignee: Optional[str] = None

