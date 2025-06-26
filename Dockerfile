FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p models outputs

EXPOSE 8501

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1