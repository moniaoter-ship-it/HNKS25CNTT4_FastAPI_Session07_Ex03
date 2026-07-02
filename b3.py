from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]

orders_db = []

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate):

    product = next(
        (p for p in products_db if p["id"] == data.product_id),
        None
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm"
        )

    if data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )

    if data.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )

    product["stock"] -= data.quantity

    order = {
        "product_id": data.product_id,
        "quantity": data.quantity,
        "total": data.quantity * product["price"]
    }

    orders_db.append(order)

    return {
        "message": "Tạo đơn hàng thành công",
        "order": order
    }