FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# install system dependencies and AstrOmatic software
RUN apt-get update && apt-get install -y \
    sextractor \
    psfex \
    python3 \
    python3-pip \
    python3-venv \
    libfftw3-dev \
    libatlas-base-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
RUN ln -s /usr/bin/source-extractor /usr/bin/sex

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir \
    numpy \
    astropy \
    galsim \
    pandas

WORKDIR /data

CMD ["/bin/bash"]