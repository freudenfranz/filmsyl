#FROM: select a base image for our image (the environment in which we will run our code), this is usually the first instruction
#python:3.8.12-buster
FROM python:3.8.12-slim
RUN pip install --upgrade pip

COPY requirements.txt /requirements.txt
#RUN: execute a command inside of the image being built (for example, pip install -r requirements.txt to install package dependencies)
RUN pip install -r requirements.txt

#COPY: copy files and directories into our image (our package and the associated files, for example)
COPY filmsyl filmsyl
COPY setup.py setup.py
RUN pip install .

#CMD: the main command that will be executed when we run our Docker image. There can only be one CMD instruction in a Dockerfile. It is usually the last instruction!
CMD uvicorn filmsyl.api.fast:app --host 0.0.0.0 --port ${PORT}
