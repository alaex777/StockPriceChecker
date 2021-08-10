FROM python:3.8.8
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --user -r requirements.txt
CMD ["python", "app.py"]