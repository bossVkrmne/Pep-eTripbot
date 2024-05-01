FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry


COPY . /app
RUN poetry install --no-dev

CMD ["poetry", "run", "python", "src/tg_bot/main.py"]