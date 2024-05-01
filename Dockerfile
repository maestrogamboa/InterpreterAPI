FROM python:3.9-slim-buster
WORKDIR /app
COPY gen-lang-client-0267084365-1fffe74ff655.json /app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=main.py
CMD ["flask", "run", "--host", "0.0.0.0"]