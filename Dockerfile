FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV PORT=5001
ENV FLASK_API_KEY=c43649ac42bc8e0259106ffd7cb9571cda6a03a1010d2c2c6415bab08dbf98e3

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
