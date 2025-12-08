FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run migrations and start app
CMD flask --app run db upgrade && flask --app run run -h 0.0.0.0 -p $PORT