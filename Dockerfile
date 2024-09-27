FROM python:3.11-alpine

COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV FLASK_APP hello

CMD ["python", "-m", "flask", "run", "-h", "0.0.0.0"]
