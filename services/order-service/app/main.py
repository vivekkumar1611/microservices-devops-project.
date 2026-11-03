from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Order Service", version="1.0.0")
orders: dict[int, dict] = {}
next_id = 1

class OrderIn(BaseModel):
    user_id: int = Field(gt=0)
    item: str = Field(min_length=1)
    quantity: int = Field(gt=0, le=1000)

@app.get("/")
def root():
    return {"service": "order-service", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

@app.get("/orders")
def list_orders():
    return list(orders.values())

@app.post("/orders", status_code=201)
def create_order(order: OrderIn):
    global next_id
    record = {"id": next_id, **order.model_dump(), "status": "CREATED"}
    orders[next_id] = record
    next_id += 1
    return record

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]
