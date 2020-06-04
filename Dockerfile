FROM python:3.7.6
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install --upgrade pip\
    &&pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
