# 使用 Python 3.9 的官方映像檔作為基礎映像檔
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .

# 使用 --no-cache-dir 來避免緩存安裝檔案，以減少映像檔大小
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案內的所有檔案到工作目錄
COPY . .

# 曝露應用程式的埠號
EXPOSE 8000

# 啟動應用程式
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
