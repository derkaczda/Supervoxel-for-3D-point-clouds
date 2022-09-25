FROM ubuntu:22.10
RUN apt update
RUN apt install -y build-essential cmake python3 python3-dev
COPY . code
WORKDIR code
RUN mkdir build
WORKDIR build
RUN cmake .. && cmake --build .