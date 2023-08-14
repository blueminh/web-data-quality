FROM python:3.9.11

COPY requirements.txt requirements.txt
SHELL ["/bin/bash", "-c"] 
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8085

ENTRYPOINT [ "python","run.py"]