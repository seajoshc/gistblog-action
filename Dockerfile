FROM python:3.9

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./gistblog.py gistblog.py

RUN chmod +x ./gistblog.py

ENTRYPOINT [ "./gistblog.py" ]
