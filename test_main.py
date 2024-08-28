from fastapi.testclient import TestClient
from main import app  # 確保這裡的導入與實際檔案名稱一致

client = TestClient(app)

def test_valid_order():
    response = client.post("/api/orders", json={
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": 1999.99,
        "currency": "TWD"
    })
    assert response.status_code == 200
    assert response.json() == {
        "message": "Order processed successfully",
        "order": {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 1999.99,
            "currency": "TWD"
        }
    }

def test_invalid_name():
    response = client.post("/api/orders", json={
        "id": "A0000001",
        "name": "Melody@Holiday Inn",  # 非英文字母
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": 1999.99,
        "currency": "TWD"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Name contains non-English characters"}
    
def test_name_capitalization():
    response = client.post("/api/orders", json={
        "id": "A0000001",
        "name": "melody holiday inn",  # 每個單字首字母非大寫
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": 1999.99,
        "currency": "TWD"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Each word in the name must start with a capital letter"}

def test_price_over_limit():
    response = client.post("/api/orders", json={
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": 2100,
        "currency": "TWD"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Price is over 2000"}

def test_currency_conversion():
    response = client.post("/api/orders", json={
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": 70,  # USD，轉換後為 70 * 31 = 2170
        "currency": "USD"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Price is over 2000"}

def test_invalid_currency_format():
    response = client.post("/api/orders", json={
        "id": "A0000001",
        "name": "Melody Holiday Inn",
        "address": {
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road"
        },
        "price": 1999.99,
        "currency": "JPY"  # 不支援的貨幣格式
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Currency format is wrong"}