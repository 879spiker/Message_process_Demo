from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
import uvicorn  # 用於本地啟動測試伺服器

app = FastAPI()

# 自訂義的驗證錯誤處理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 解析驗證錯誤訊息並只提取必要的部分
    error_message = exc.errors()[0]['msg'] if exc.errors() else "Validation error occurred"
    return JSONResponse(
        status_code=400,
        content={"detail": error_message},
    )


# 定義訂單的數據模型
class Address(BaseModel):
    city: str
    district: str
    street: str

    @validator("city", "district", "street")
    def validate_location(cls, v):
        if not re.match(r'^[a-z]+(?:-[a-z]+)*$', v):
            raise ValueError("Invalid location format")
        return v

class Order(BaseModel):
    id: str = Field(..., pattern=r'^A\d{7}$')
    name: str
    address: Address
    price: float
    currency: str

    @validator("name")
    def validate_name(cls, v):
        # 檢查是否只包含英文字母和空格
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError("Name contains non-English characters")
        # 檢查每個單字是否首字母大寫
        if not all(word.istitle() for word in v.split()):
            raise ValueError("Each word in the name must start with a capital letter")
        return v

# 工廠模式來創建驗證器
class OrderValidator:
    EXCHANGE_RATE = 31  # 固定匯率

    def validate(self, order: Order):
        # 檢查貨幣格式
        if order.currency not in ["TWD", "USD"]:
            raise ValueError("Currency format is wrong")

        # 先進行貨幣轉換
        if order.currency == "USD":
            order.price *= self.EXCHANGE_RATE  # 將金額轉換為 TWD
            order.currency = "TWD"
        
        # 再檢查轉換後的價格是否超過 2000
        if order.price > 2000:
            raise ValueError("Price is over 2000")

        return order

class OrderValidatorFactory:
    @staticmethod
    def get_validator(currency: str) -> OrderValidator:
        return OrderValidator()

@app.post("/api/orders")
def process_order(order: Order):
    try:
        validator = OrderValidatorFactory.get_validator(order.currency)
        validated_order = validator.validate(order)
        return {"message": "Order processed successfully", "order": validated_order.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 本地端啟動測試伺服器的入口
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)