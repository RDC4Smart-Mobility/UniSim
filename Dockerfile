FROM ubuntu:latest

LABEL Name=UniSim Version=0.1.1

# SUMO インストール前の準備
ENV DEBIAN_FRONTEND noninteractive
RUN set -x && \
    apt-get -y update && \
    apt-get -y install \
        tzdata \
        python-pip \
        python-tk \
        software-properties-common

WORKDIR /tmp
ADD requirements.txt /tmp
RUN pip install -r requirements.txt

# SUMO インストール
RUN set -x && \
    add-apt-repository -y ppa:sumo/stable && \
    apt-get -y update && \
    apt-get -y install \
        sumo \
        sumo-tools \
        sumo-doc \
        && \
    apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*

ENV SUMO_HOME /usr/share/sumo

# UniSim インストール
COPY UniSim/ /opt/UniSim/
WORKDIR /opt/UniSim
RUN pip install -e .

# CMD
RUN mkdir /simdata
WORKDIR /simdata
