FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8899

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8899", "--reload"]
