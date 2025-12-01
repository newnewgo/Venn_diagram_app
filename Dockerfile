# 使用 Python 3.11 官方精簡版
FROM python:3.11-slim

# 工作目錄
WORKDIR /app

# 複製 requirements.txt
COPY requirements.txt .

# 安裝依賴套件（避免 Cache / 降低檔案大小）
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼到容器
COPY . .

# Cloud Run 要求服務跑在 8080 port
ENV PORT=8080

# Streamlit 也要跟著改成跑在 8080
EXPOSE 8080

# 讓 Streamlit 跑起 app.py
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
