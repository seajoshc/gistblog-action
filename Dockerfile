FROM python:3.9

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./gistblog.py /app/gistblog.py

RUN chmod +x /app/gistblog.py

ENTRYPOINT [ "/app/gistblog.py" ]
