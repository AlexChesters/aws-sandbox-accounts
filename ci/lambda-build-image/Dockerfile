FROM public.ecr.aws/ubuntu/ubuntu:22.04_stable

# set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# install curl/wget
RUN apt update -y && apt install curl wget -y

# install python
RUN apt update -y && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y && apt install python3.11 python3-venv python3-pip -y

# set python3.11 as default
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.11 /usr/bin/python3
