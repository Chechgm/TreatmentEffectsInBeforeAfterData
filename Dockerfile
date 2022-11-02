# Set the base image
FROM ubuntu:20.04

# Avoid questions in the docker build
ARG DEBIAN_FRONTEND=noninteractive

# Install general packages
RUN apt-get update \
	&& apt-get install -y wget \
	&& apt-get install -y build-essential \
	&& apt-get install -y gcc-multilib g++-multilib lib32z1 \
    && apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install python and pip
 RUN apt-get update \
     && apt-get install -y software-properties-common  \
     && add-apt-repository ppa:deadsnakes/ppa \
     && apt-get install -y python3.9 \
     && apt-get install -y python3-pip

# Project specific folders and installations
RUN mkdir /home/TreatmentEffectsInBeforeAfterData
ENV PYTHONPATH="${PYTHONPATH}:/home/TreatmentEffectsInBeforeAfterData"

COPY requirements.txt /home/TreatmentEffectsInBeforeAfterData/requirements.txt
RUN pip3 install -r /home/TreatmentEffectsInBeforeAfterData/requirements.txt