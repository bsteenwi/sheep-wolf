FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir mesa solara networkx matplotlib altair

EXPOSE 8000

CMD ["python", "app.py"]