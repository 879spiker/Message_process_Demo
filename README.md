
# README

## 專案說明

此專案使用 FastAPI 建立一個簡單的訂單處理 API，並包含單元測試來驗證 API 功能。在專案中，我們應用了 SOLID 原則與設計模式來保持程式碼的可維護性、擴展性及清晰度。

### 目錄結構

```
. ├── main.py # 主程式檔案，包含 API 與數據驗證 
  ├── test_main.py # 測試檔案，使用 FastAPI TestClient 進行單元測試 
  ├── requirements.txt # Python 依賴項目清單 
  ├── Dockerfile # Docker 映像檔構建指令 
  └── README.md # 專案說明文件
```


## 使用技術

- Python 3.8+
- FastAPI
- Pydantic
- Uvicorn (本地伺服器啟動)
- Pytest (測試框架)
- Docker

## 安裝與執行

### 使用 Docker 啟動專案

1. **構建 Docker 映像檔**

    在專案根目錄下，執行以下指令來構建 Docker 映像檔：

    ```bash
    docker build -t my-fastapi-app .
    ```

    這會根據 `Dockerfile` 建立一個名為 `my-fastapi-app` 的映像檔。

2. **運行 Docker 容器**

    執行以下指令來運行容器：

    ```bash
    docker run -p 8000:8000 my-fastapi-app
    ```

    這將在埠號 `8000` 上運行你的 FastAPI 應用程式，可以在瀏覽器中透過 `http://localhost:8000` 訪問。

### 手動安裝與執行

1. 安裝依賴：

    ```bash
    pip install -r requirements.txt
    ```

2. 啟動伺服器：

    ```bash
    uvicorn main:app --reload
    ```

3. 執行測試：

    ```bash
    pytest test_main.py
    ```

## SOLID 原則

在這個專案中，我們應用了以下的 SOLID 原則：

1. **單一職責原則 (Single Responsibility Principle)**:
    - 每個類別和函式都有清晰的單一職責。例如，`Order` 類別僅負責訂單的數據結構與驗證，而 `OrderValidator` 負責訂單驗證邏輯。

2. **開放封閉原則 (Open/Closed Principle)**:
    - 系統是開放於擴展、封閉於修改的。使用 `OrderValidator` 類別進行訂單驗證，可以通過擴展 `OrderValidator` 的方法來增加新的驗證邏輯，而不需要修改現有的代碼。

3. **里氏替換原則 (Liskov Substitution Principle)**:
    - 在這個專案中，主要透過工廠模式達到里氏替換原則。例如，`OrderValidatorFactory` 可以根據不同的需求來替換具體的驗證器。

4. **介面隔離原則 (Interface Segregation Principle)**:
    - 我們使用類別來區分不同的責任，避免讓一個類別負擔過多的功能。每個類別僅提供其職責所需的功能。

5. **依賴反轉原則 (Dependency Inversion Principle)**:
    - 我們透過 `OrderValidatorFactory` 工廠模式來解耦驗證器的具體實現，使得上層邏輯不依賴於具體的驗證器實作。

## 設計模式

本專案應用了以下設計模式：

1. **工廠模式 (Factory Pattern)**:
    - 使用 `OrderValidatorFactory` 來根據不同的情境返回不同的驗證器實例。這樣可以輕易地添加新的驗證器而不需要更改現有的邏輯。

2. **策略模式 (Strategy Pattern)**:
    - 雖然目前只有一個驗證器 (`OrderValidator`)，但設計已經考慮到未來可能會有不同驗證策略的需求，工廠模式也促進了策略模式的應用。

## 測試

測試檔案 `test_main.py` 使用了 FastAPI 的 TestClient 來測試 API 各種輸入情境，包含了有效訂單、名稱錯誤、價格超出限制、以及無效的貨幣格式等測試案例。
