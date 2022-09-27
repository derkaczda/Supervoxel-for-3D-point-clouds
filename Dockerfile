FROM ubuntu:20.04
RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y && apt update
RUN apt install -y build-essential cmake python3.8 python3.8-dev
RUN apt install -y libboost-all-dev
RUN apt install -y tmux vim python3-pip
RUN pip3 install open3d numpy
RUN apt install ffmpeg libsm6 libxext6  -y
COPY . code
WORKDIR code
RUN mkdir build
WORKDIR build
RUN cmake .. && cmake --build .
WORKDIR /code
RUN chmod -R 0777 .