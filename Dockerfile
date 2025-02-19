FROM python:3.10-slim

LABEL maintainer="nanocoes.com.ng"

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN pip install --upgrade pip 

RUN python -m venv /py && \
    /py/bin/pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

EXPOSE 8080

CMD ["daphne", "nineapp.asgi:application", "-b", "0.0.0.0", "-p", "8080"]