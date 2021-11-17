FROM python:3
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=fake12345
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
