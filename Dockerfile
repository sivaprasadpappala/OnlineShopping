FROM python:3.11-alpine

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Switch to non-root user
USER appuser

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

# Bind to all interfaces (CRITICAL for K8s)
CMD ["python", "app.py", "--host=0.0.0.0"]