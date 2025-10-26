from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, func
import datetime

class Base(DeclarativeBase):
    pass

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50))
    last_checked: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )

    incidents = relationship("Incident", back_populates="service")

class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    description: Mapped[str] = mapped_column(String(100))
    start_time: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )
    resolved_time: Mapped[datetime.datetime] = mapped_column(nullable=True)

    service = relationship("Service", back_populates="incidents")
