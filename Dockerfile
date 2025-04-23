FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv pip install --system --no-cache-dir --upgrade -r requirements.txt


EXPOSE 8501

CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]