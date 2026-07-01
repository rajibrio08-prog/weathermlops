FROM python:3.10-slim
WORKDIR /app
COPY . .
# mlflow যোগ করা হয়েছে dependencies-এ
RUN pip install --no-cache-dir pandas scikit-learn joblib fastapi uvicorn pydantic mlflow
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]