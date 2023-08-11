FROM python:3.11
ENV PYTHONPATH "${PYTHONPATH}:/AntoshaBot"
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .