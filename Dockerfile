FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data at build time (better than runtime)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]