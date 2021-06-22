ARG BASE_CONTAINER=ubuntu:18.04
FROM $BASE_CONTAINER

ENV DEBIAN_FRONTEND=noninteractive TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    g++ \
    gfortran \
    make \
    curl \
    git \
    libblas-dev \
    liblapack-dev \
    libtool \
    m4 \
    libnetcdf-dev \
    libnetcdff-dev \
    perl \
    rsync \
    libffi-dev \
    openssl \
    bats \
    python3 \
    libpython3-dev \
    python3-dev \
    python3-setuptools \
    python3-pip \
    cython3 \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev

RUN wget -q http://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz && \
 tar xzf mpich-3.1.4.tar.gz && \
    cd mpich-3.1.4 && \
    ./configure --enable-fortran --enable-cxx --prefix=/usr --enable-fast=all,O3 && \
    make -j24 && \
    make install && ldconfig && rm -rf /mpich-3.1.4

# install dependencies for serialbox
RUN apt-get update && apt-get install -y \
    libssl-dev \
    clang \
    clang-format \
    clang-tidy \
    python3-numpy \
    python3-nose \
    python3-sphinx

RUN wget https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3.tar.gz && \
    tar xzf cmake-3.17.3.tar.gz && \
    cd cmake-3.17.3 && \
    ./bootstrap && make -j4 && make install


# Install headers from the Boost library
RUN wget -q https://boostorg.jfrog.io/artifactory/main/release/1.74.0/source/boost_1_74_0.tar.gz && \
    tar xzf boost_1_74_0.tar.gz && \
    cd boost_1_74_0 && \
    cp -r boost /usr/include/ && cd /

## Build Serialbox
###
RUN git clone -b v2.6.0 --depth 1 https://github.com/GridTools/serialbox.git /usr/src/serialbox && \
    cmake -B build -S /usr/src/serialbox -DSERIALBOX_USE_NETCDF=ON -DSERIALBOX_TESTING=ON \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local/serialbox && \
    cmake --build build/ -j $(nproc) --target install

RUN pip3 install --upgrade pip setuptools wheel && \
    ln -s /bin/python3 /bin/python && \
    ln -s /bin/pip3 /bin/pip
RUN pip3 install numpy==1.19.5 matplotlib==3.3.4 ipykernel==5.5.5 ipyparallel==6.3.0 mpi4py==3.0.3 jupyter==1.0.0

COPY gt4py /gt4py
COPY fv3gfs-util /fv3gfs-util

RUN pip3 install -e /gt4py
RUN python3 -m gt4py.gt_src_manager install

RUN cd /fv3gfs-util && \
    git reset --hard 7c1367348037474711da454ca3dc5b50bf79e17d && \
    cd - && \
    pip3 install -e /fv3gfs-util


RUN ipython profile create --parallel --profile=mpi

COPY setup/ipcluster_config.py /root/.ipython/profile_mpi/ipcluster_config.py

ENV SERIALBOX_ROOT /usr/local/serialbox
ENV DOCKER True
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

WORKDIR /workshop
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]