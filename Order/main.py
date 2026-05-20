from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# =========================
# 1. DATABASE SETUP
# =========================

DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# =========================
# 2. DATABASE MODEL
# =========================

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="Placed")


Base.metadata.create_all(bind=engine)


# =========================
# 3. Pydantic SCHEMAS
# =========================

class OrderCreate(BaseModel):
    item_name: str
    quantity: int


class OrderResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    status: str

    class Config:
        from_attributes = True


# =========================
# 4. FASTAPI APP
# =========================

app = FastAPI(title="Order / Request Tracking API")


# =========================
# 5. DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 6. API ENDPOINTS
# =========================

@app.post("/place-order/", response_model=OrderResponse)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(
        item_name=order.item_name,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@app.get("/orders/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/")
def root():
    return {"status": "API is running"}
