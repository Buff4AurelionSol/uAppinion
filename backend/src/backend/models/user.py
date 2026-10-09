from backend.config.db import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean, DateTime, func
from datetime import datetime


class User(Base): 
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        unique=True, 
        index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
