from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Create the data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Database setup
DATABASE_URL = "sqlite:///data/heritage.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    monument = Column(String)
    timestamp = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    air_pollution = Column(Float)
    vibration = Column(Float)
    crack_width = Column(Float)
    risk_level = Column(Integer)
    anomaly = Column(Integer)
    shi = Column(Float)


# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully!")
