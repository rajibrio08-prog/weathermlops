<<<<<<< HEAD
FROM python:3.10-slim
WORKDIR /app
COPY . .
# mlflow যোগ করা হয়েছে dependencies-এ
RUN pip install --no-cache-dir pandas scikit-learn joblib fastapi uvicorn pydantic mlflow
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
=======
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pandas scikit-learn joblib fastapi uvicorn pydantic
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 99b9a56bc909234e8b8e6a7b38794f41c4d2f4c5
