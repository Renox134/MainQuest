FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# ---- Core system deps ----
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3-pip \
    build-essential \
    git \
    aidl \
    unzip \
    wget \
    zip \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libstdc++6 \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# ---- python tools (system-wide) ----
RUN pip3 install \
    setuptools \
    Cython==0.29.33 \
    buildozer==1.5.0

# switch ownership to avoid permisson errors
RUN mkdir -p /home/ubuntu/.buildozer \
    && chown -R ubuntu:ubuntu /home/ubuntu/.buildozer \
    && chmod -R u+rw /home/ubuntu/.buildozer 

# Use the existing non-root 'ubuntu' user that ships with Ubuntu 24.04
USER ubuntu
WORKDIR /home/ubuntu/app

CMD ["buildozer", "android", "debug"]