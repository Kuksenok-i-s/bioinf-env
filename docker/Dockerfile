FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
# Переменная заставляет оутпут всегда выводиться в stdout без буферизации (Логи всегда будет видно)

RUN apt-get update && apt-get install -yqq --no-install-recommends \
    build-essential \
    wget \
    git \
    curl \
    vim \
    default-jdk \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libsqlite3-dev \
    sqlite3 \
    libcurl4-openssl-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
ENV PATH="/opt/conda/bin:$PATH"

RUN conda create -n bioinfo python=3.12 sqlite -y && conda clean -a -y

# Далее стартуем в правильном окружении, в нашем случае - bioinfo

SHELL ["conda", "run", "-n", "bioinfo", "/bin/bash", "-c"]


RUN conda install -y \
 -c anaconda \
 sqlite

# Устанавливаем зависимости, включая pysqlite3
RUN conda install -c conda-forge pysqlite3 -y

RUN conda install -y \
 -c conda-forge\
 biopython\
 pandas \
 numpy \
 plotly \
 matplotlib \
 seaborn \
 scikit-bio \
 scipy \
 jupyterlab

RUN conda install -y \
 -c bioconda \
 blast \
 hmmer \
 bowtie2 \
 samtools

COPY startup.py /usr/local/src/startup.py

WORKDIR /workspace

EXPOSE 8888

# CMD ["python", "/usr/local/src/startup.py"]
ENTRYPOINT ["python", "/usr/local/src/startup.py"]