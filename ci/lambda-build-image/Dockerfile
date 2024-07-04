FROM public.ecr.aws/ubuntu/ubuntu:22.04_stable

ENV DEBIAN_FRONTEND=noninteractive

# install python
RUN apt update -y && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y && apt install python3.12 python3-venv python3-pip -y

# install pipx
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

# install poetry
RUN pipx install poetry==1.8.2
