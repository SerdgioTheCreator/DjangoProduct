FROM python:3.13-slim
RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY . .
EXPOSE 8000
CMD ["gunicorn", "djangoproduct.wsgi:application", "--bind", "0.0.0.0:8000"]