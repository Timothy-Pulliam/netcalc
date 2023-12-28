FROM python:3.11-alpine

ENV PATH=$PATH:/home/flaskuser/.local/bin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=1

EXPOSE 8080/tcp
RUN adduser -D flaskuser

WORKDIR /home/flaskuser
COPY . .
RUN chmod +x start.sh
RUN chown -R flaskuser:flaskuser ./
USER flaskuser

RUN pip install --user -r requirements.txt
RUN pip install --user gunicorn

CMD ["/bin/sh", "start.sh"]