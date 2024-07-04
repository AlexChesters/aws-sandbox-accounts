FROM public.ecr.aws/ubuntu/ubuntu:22.04_stable

# set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# install curl/wget
RUN apt update -y && apt install curl wget -y

# install python
RUN apt update -y && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y && apt install python3.12 python3-venv python3-pip -y
