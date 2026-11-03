from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Product Service", version="1.0.0")
products: dict[int, dict] = {}
next_id = 1

class ProductIn(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    price: float = Field(gt=0)

@app.get("/")
def root():
    return {"service": "product-service", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}

@app.get("/products")
def list_products():
    return list(products.values())

@app.post("/products", status_code=201)
def create_product(product: ProductIn):
    global next_id
    record = {"id": next_id, **product.model_dump()}
    products[next_id] = record
    next_id += 1
    return record

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]
