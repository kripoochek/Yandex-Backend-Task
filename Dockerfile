FROM python:3.8

EXPOSE 8000

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/main.py .

CMD ["uvicorn", "app.main:star_app", "--host", "127.0.0.1","--reload", "--port", "8000"]
