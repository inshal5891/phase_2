from sqlmodel import SQLModel as _SQLModel
from typing import Optional
from datetime import datetime
import os

class SQLModel(_SQLModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }