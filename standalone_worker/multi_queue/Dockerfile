FROM ubuntu:18.04

MAINTAINER gaurav negi "gauravn@cdac.in"

# We copy just the requirements.txt first to leverage Docker cache


WORKDIR /standalone_worker


RUN apt-get update -y && \
    apt-get install -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update
    

RUN apt-get install -y libglib2.0-0 && \
    apt-get install -y libxrender1 && \
    apt-get install -y python3.7 && \
    apt install -y libsm6 libxext6



RUN apt-get install -y python3-pip && \
    apt-get install -y cmake

RUN pip3 install -U pip

RUN apt-get install -y python-psycopg2

COPY ./requirements.txt /standalone_worker/requirements.txt

RUN python3.7 -m pip install -U pip && \
    python3.7 -m pip install -r requirements.txt

RUN mkdir /models
RUN mkdir /image_uploads

COPY . /standalone_worker

CMD python3.7 /standalone_worker/image_saving_worker.py

#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
#sudo docker run -it --rm -v /home/iamtheuserofthis/python_workspace/for_containerization/image_uploads:/image_uploads -v /home/iamtheuserofthis/python_workspace/for_containerization/log_files:/log_files -v /home/iamtheuserofthis/python_workspace/for_containerization/models:/models 90f60479d519
