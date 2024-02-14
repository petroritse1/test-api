FROM python:3.9
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install flask_jwt_extended  --upgrade
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

#adding commemts to docker files