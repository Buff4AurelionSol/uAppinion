from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.config.db import get_db
from datetime import date
from typing import Literal

router = APIRouter()

StatusType = Literal["read", "reading", "plan_to_read", "dropped"]
