FROM public.ecr.aws/bitnami/python:3.10.6

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY app /src/app

EXPOSE 80/tcp
ENV TZ Asia/Seoul
RUN apt-get update && apt-get install -y tzdata

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]