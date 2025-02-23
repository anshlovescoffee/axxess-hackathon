FROM python:3.12

RUN apt update
RUN apt install -y python3-venv build-essential

WORKDIR /env
RUN python -m venv venv

WORKDIR /app
COPY requirements.txt requirements.txt
RUN /env/venv/bin/pip install uv
RUN /env/venv/bin/uv pip install -r requirements.txt --system 

COPY . . 
RUN /env/venv/bin/uv run gen_patients.py 

CMD ["/env/venv/bin/uv", "run", "python", "app.py"]
