FROM python:3.8
WORKDIR /src

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY ./app ./app

#CMD ["python","-m", "app.main"]
