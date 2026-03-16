FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# System dependencies for buildozer
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3-pip \
    build-essential \
    autoconf \
    automake \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo6 \
    cmake \
    git \
    unzip \
    openjdk-17-jdk \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN pip3 install \
    setuptools \
    Cython==0.29.33 \
    buildozer

# Install Android commandline tools
RUN mkdir -p /opt/android-sdk/cmdline-tools \
    && cd /opt/android-sdk \
    && wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \
    && unzip commandlinetools-linux-11076708_latest.zip \
    && rm commandlinetools-linux-11076708_latest.zip \
    && mv cmdline-tools latest \
    && mkdir cmdline-tools \
    && mv latest cmdline-tools/

ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

# Accept licenses automatically
RUN yes | sdkmanager --licenses

# Install required SDK components
RUN sdkmanager \
    "platform-tools" \
    "platforms;android-33" \
    "build-tools;33.0.2"

# Use the existing non-root 'ubuntu' user that ships with Ubuntu 24.04
USER ubuntu
WORKDIR /home/ubuntu/app

CMD ["buildozer", "android", "debug"]