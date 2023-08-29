FROM python:3.11-slim-buster

ENV AWS_REGION=test
ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_ROLE_NAME=test

RUN mkdir /app
COPY ./app /app
COPY ./pyproject.toml /app

WORKDIR /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false && poetry install
# RUN poetry install --no-dev
# RUN poetry install

ENTRYPOINT ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.baseUrlPath=/sagemaker"]

