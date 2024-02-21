FROM python:3.9
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install flask_jwt_extended  --upgrade
COPY . .
# CMD ["/bin/bash","docker-entrypoint.sh"]
CMD ["/bin/bash","docker-entrypoint.sh"]

#adding commemts to docker files