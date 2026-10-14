FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app.py .
COPY index.html .
EXPOSE 8000
CMD ["python", "app.py"]
