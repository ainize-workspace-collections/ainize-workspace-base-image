import argparse
from argparse import Namespace

CUDA_VERSION_LIST = [
    "11.3.1",
]

MINICONDA_INFO_DICT = {
    "4.10.3": {
        "37": "9f186c1d86c266acc47dbc1603f0e2ed",
        "38": "14da4a9a44b337f7ccb8363537f65b9c",
        "39": "8c69f65a4ae27fb41df0fe552b4a8a3b",
    }
}

CUDA_INFO_DICT = {
    "11.3.1": {
        # For Basics
        "NV_CUDA_CUDART_VERSION": "11.3.109-1",
        "NV_CUDA_COMPAT_PACKAGE": "cuda-compat-11-3",
        # For Runtimes
        "NV_CUDA_LIB_VERSION": "11.3.1-1",

        "NV_NVTX_VERSION": "11.3.109-1",
        "NV_LIBNPP_VERSION": "11.3.3.95-1",
        "NV_LIBCUSPARSE_VERSION": "11.6.0.109-1",

        "NV_LIBCUBLAS_VERSION": "11.5.1.109-1",

        "NV_LIBNCCL_PACKAGE_NAME": "libnccl2",
        "NV_LIBNCCL_PACKAGE_VERSION": "2.9.9-1",
        "NCCL_VERSION": "2.9.9-1",

        # For Devel
        "NV_CUDA_CUDART_DEV_VERSION": "11.3.109-1",
        "NV_NVML_DEV_VERSION": "11.3.58-1",
        "NV_LIBNPP_DEV_VERSION": "11.3.3.95-1",
        "NV_LIBCUSPARSE_DEV_VERSION": "11.6.0.109-1",
        "NV_LIBCUBLAS_DEV_PACKAGE_NAME": "libcublas-dev-11-3",
        "NV_LIBCUBLAS_DEV_VERSION": "11.5.1.109-1",
        "NV_LIBNCCL_DEV_PACKAGE_NAME": "libnccl-dev",
        "NV_LIBNCCL_DEV_PACKAGE_VERSION": "2.9.9-1",

        # For Cudnn 8 Devel
        "NV_CUDNN_VERSION": "8.2.0.53",
        "NV_CUDNN_PACKAGE_NAME": "libcudnn8",
    }
}


def define_arg_parser() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cuda_version",
        choices=CUDA_VERSION_LIST,
        required=True,
        help="cuda version"
    )
    parser.add_argument(
        "--miniconda_version",
        choices=list(MINICONDA_INFO_DICT.keys()),
        default="4.10.3",
        help="miniconda version"
    )
    parser.add_argument(
        "--python_version",
        default="3.8",
        help="python version"
    )
    return parser.parse_args()


def basic_string() -> str:
    return """\
FROM ubuntu:20.04

### BASICS ###
# Technical Environment Variables
ENV \\
    SHELL="/bin/bash" \\
    HOME="/root"  \\
    # Nobteook server user: https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile#L33
    NB_USER="root" \\
    USER_GID=0 \\
    DISPLAY=":1" \\
    TERM="xterm" \\
    DEBIAN_FRONTEND="noninteractive" \\
    WORKSPACE_HOME="/workspace"

WORKDIR $HOME

# Layer cleanup script
COPY scripts/clean-layer.sh  /usr/bin/clean-layer.sh
COPY scripts/fix-permissions.sh  /usr/bin/fix-permissions.sh

# Make clean-layer and fix-permissions executable
RUN \\
    chmod a+rwx /usr/bin/clean-layer.sh && \\
    chmod a+rwx /usr/bin/fix-permissions.sh

# Generate and Set locals
# https://stackoverflow.com/questions/28405902/how-to-set-the-locale-inside-a-debian-ubuntu-docker-container#38553499
RUN \\
    apt-get update && \\
    apt-get install -y locales && \\
    # install locales-all?
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \\
    locale-gen && \\
    dpkg-reconfigure --frontend=noninteractive locales && \\
    update-locale LANG=en_US.UTF-8 && \\
    # Cleanup
    clean-layer.sh

ENV LC_ALL="en_US.UTF-8" \\
    LANG="en_US.UTF-8" \\
    LANGUAGE="en_US:en"

# Install basics
RUN \\
    # TODO add repos?
    # add-apt-repository ppa:apt-fast/stable
    # add-apt-repository 'deb http://security.ubuntu.com/ubuntu xenial-security main'
    apt-get update --fix-missing && \\
    apt-get install -y sudo apt-utils && \\
    apt-get upgrade -y && \\
    apt-get update && \\
    apt-get install -y --no-install-recommends \\
    # This is necessary for apt to access HTTPS sources:
    apt-transport-https \\
    gnupg-agent \\
    gpg-agent \\
    gnupg2 \\
    ca-certificates \\
    build-essential \\
    pkg-config \\
    software-properties-common \\
    lsof \\
    net-tools \\
    libcurl4 \\
    curl \\
    wget \\
    cron \\
    openssl \\
    psmisc \\
    iproute2 \\
    tmux \\
    dpkg-sig \\
    uuid-dev \\
    csh \\
    xclip \\
    clinfo \\
    time \\
    libssl-dev \\
    libgdbm-dev \\
    libncurses5-dev \\
    libncursesw5-dev \\
    # required by pyenv
    libreadline-dev \\
    libedit-dev \\
    xz-utils \\
    gawk \\
    # Simplified Wrapper and Interface Generator (5.8MB) - required by lots of py-libs
    swig \\
    # Graphviz (graph visualization software) (4MB)
    graphviz libgraphviz-dev \\
    # Terminal multiplexer
    screen \\
    # Editor
    nano \\
    # Find files
    locate \\
    # Dev Tools
    sqlite3 \\
    # XML Utils
    xmlstarlet \\
    # GNU parallel
    parallel \\
    #  R*-tree implementation - Required for earthpy, geoviews (3MB)
    libspatialindex-dev \\
    # Search text and binary files
    yara \\
    # Minimalistic C client for Redis
    libhiredis-dev \\
    # postgresql client
    libpq-dev \\
    # mariadb client (7MB)
    # libmariadbclient-dev \\
    # image processing library (6MB), required for tesseract
    libleptonica-dev \\
    # GEOS library (3MB)
    libgeos-dev \\
    # style sheet preprocessor
    less \\
    # Print dir tree
    tree \\
    # Bash autocompletion functionality
    bash-completion \\
    # ping support
    iputils-ping \\
    # Map remote ports to localhosM
    socat \\
    # Json Processor
    jq \\
    rsync \\
    # sqlite3 driver - required for pyenv
    libsqlite3-dev \\
    # VCS:
    git \\
    subversion \\
    jed \\
    # odbc drivers
    unixodbc unixodbc-dev \\
    # Image support
    libtiff-dev \\
    libjpeg-dev \\
    libpng-dev \\
    libglib2.0-0 \\
    libxext6 \\
    libsm6 \\
    libxext-dev \\
    libxrender1 \\
    libzmq3-dev \\
    # protobuffer support
    protobuf-compiler \\
    libprotobuf-dev \\
    libprotoc-dev \\
    autoconf \\
    automake \\
    libtool \\
    cmake  \\
    fonts-liberation \\
    google-perftools \\
    # Compression Libs
    # also install rar/unrar? but both are propriatory or unar (40MB)
    zip \\
    gzip \\
    unzip \\
    bzip2 \\
    lzop \\
    # deprecates bsdtar (https://ubuntu.pkgs.org/20.04/ubuntu-universe-i386/libarchive-tools_3.4.0-2ubuntu1_i386.deb.html)
    libarchive-tools \\
    zlibc \\
    # unpack (almost) everything with one command
    unp \\
    libbz2-dev \\
    liblzma-dev \\
    zlib1g-dev \\ 
    # OpenMPI support
    libopenmpi-dev \\
    openmpi-bin \\
    # libartals
    liblapack-dev \\
    libatlas-base-dev \\
    libeigen3-dev \\
    libblas-dev \\
    # HDF5
    libhdf5-dev \\
    # TBB   
    libtbb-dev \\
    # TODO: installs tenserflow 2.4 - Required for tensorflow graphics (9MB)
    libopenexr-dev \\
    # GCC OpenMP
    libgomp1 \\
    # ttyd
    libwebsockets-dev \\
    libjson-c-dev \\
    libssl-dev \\
    # data science
    libopenmpi-dev \\
    openmpi-bin \\
    libomp-dev \\
    libopenblas-base \\
    # ETC
    vim && \\
    # Update git to newest version
    add-apt-repository -y ppa:git-core/ppa  && \\
    apt-get update && \\
    apt-get install -y --no-install-recommends git && \\
    # Fix all execution permissions
    chmod -R a+rwx /usr/local/bin/ && \\
    # configure dynamic linker run-time bindings
    ldconfig && \\
    # Fix permissions
    fix-permissions.sh $HOME && \\
    # Cleanup
    clean-layer.sh

### END BASICS ###
"""


def cuda_string(cuda_version: str) -> str:
    cuda_info = CUDA_INFO_DICT[cuda_version]
    major_version, minor_version, patch_version = cuda_version.split('.')
    CUDA_HYPHEN = f"{major_version}-{minor_version}"
    CUDA_DOT = f"{major_version}.{minor_version}"

    # For Basics
    NVIDIA_REQUIRE_CUDA = f"cuda>={CUDA_DOT} brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450"
    NV_CUDA_CUDART_VERSION = cuda_info["NV_CUDA_CUDART_VERSION"]
    NV_CUDA_COMPAT_PACKAGE = cuda_info["NV_CUDA_COMPAT_PACKAGE"]

    CUDA_VERSION = cuda_version

    # For Runtime
    NV_CUDA_LIB_VERSION = cuda_info["NV_CUDA_LIB_VERSION"]
    NV_NVTX_VERSION = cuda_info["NV_NVTX_VERSION"]
    NV_LIBNPP_VERSION = cuda_info["NV_LIBNPP_VERSION"]
    NV_LIBNPP_PACKAGE = f"libnpp-{CUDA_HYPHEN}={NV_LIBNPP_VERSION}"
    NV_LIBCUSPARSE_VERSION = cuda_info["NV_LIBCUSPARSE_VERSION"]

    NV_LIBCUBLAS_PACKAGE_NAME = f"libcublas-{CUDA_HYPHEN}"
    NV_LIBCUBLAS_VERSION = cuda_info["NV_LIBCUBLAS_VERSION"]
    NV_LIBCUBLAS_PACKAGE = f"{NV_LIBCUBLAS_PACKAGE_NAME}={NV_LIBCUBLAS_VERSION}"

    NCCL_VERSION = cuda_info["NCCL_VERSION"]
    NV_LIBNCCL_PACKAGE_NAME = cuda_info["NV_LIBNCCL_PACKAGE_NAME"]
    NV_LIBNCCL_PACKAGE_VERSION = cuda_info["NV_LIBNCCL_PACKAGE_VERSION"]
    NV_LIBNCCL_PACKAGE = f"{NV_LIBNCCL_PACKAGE_NAME}={NV_LIBNCCL_PACKAGE_VERSION}+cuda{CUDA_DOT}"

    # For Devel
    NV_CUDA_CUDART_DEV_VERSION = cuda_info["NV_CUDA_CUDART_DEV_VERSION"]
    NV_NVML_DEV_VERSION = cuda_info["NV_NVML_DEV_VERSION"]
    NV_LIBNPP_DEV_VERSION = cuda_info["NV_LIBNPP_DEV_VERSION"]
    NV_LIBNPP_DEV_PACKAGE = f"libnpp-dev-{CUDA_HYPHEN}={NV_LIBNPP_DEV_VERSION}"
    NV_LIBCUSPARSE_DEV_VERSION = cuda_info["NV_LIBCUSPARSE_DEV_VERSION"]
    NV_LIBCUBLAS_DEV_PACKAGE_NAME = cuda_info["NV_LIBCUBLAS_DEV_PACKAGE_NAME"]
    NV_LIBCUBLAS_DEV_VERSION = cuda_info["NV_LIBCUBLAS_DEV_VERSION"]
    NV_LIBCUBLAS_DEV_PACKAGE = f"{NV_LIBCUBLAS_DEV_PACKAGE_NAME}={NV_LIBCUBLAS_DEV_VERSION}"

    NV_LIBNCCL_DEV_PACKAGE_NAME = cuda_info["NV_LIBNCCL_DEV_PACKAGE_NAME"]
    NV_LIBNCCL_DEV_PACKAGE_VERSION = cuda_info["NV_LIBNCCL_DEV_PACKAGE_VERSION"]
    NCCL_VERSION = cuda_info["NCCL_VERSION"]
    NV_LIBNCCL_DEV_PACKAGE = f"{NV_LIBNCCL_DEV_PACKAGE_NAME}={NV_LIBNCCL_DEV_PACKAGE_VERSION}+cuda{CUDA_DOT}"

    # For Cudnn 8 Devel
    NV_CUDNN_VERSION = cuda_info["NV_CUDNN_VERSION"]
    NV_CUDNN_PACKAGE = f"libcudnn8={NV_CUDNN_VERSION}-1+cuda{CUDA_DOT}"
    NV_CUDNN_PACKAGE_DEV = f"libcudnn8-dev={NV_CUDNN_VERSION}-1+cuda{CUDA_DOT}"
    NV_CUDNN_PACKAGE_NAME = cuda_info["NV_CUDNN_PACKAGE_NAME"]
    ret = ""
    # base
    ret += f"""\
### CUDA BASE ###
# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/{CUDA_VERSION}/ubuntu2004/base/Dockerfile
ENV NVIDIA_REQUIRE_CUDA "{NVIDIA_REQUIRE_CUDA}"

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gnupg2 curl ca-certificates && \\
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub | apt-key add - && \\
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \\
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \\
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    apt-get clean && \\
    rm -rf $HOME/.cache/* && \\
    rm -rf /tmp/* && \\
    rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION {CUDA_VERSION}

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \\
    cuda-cudart-{CUDA_HYPHEN}={NV_CUDA_CUDART_VERSION} \\
    {NV_CUDA_COMPAT_PACKAGE} && \\
    ln -s cuda-{CUDA_DOT} /usr/local/cuda && \\
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    apt-get clean && \\
    rm -rf $HOME/.cache/* && \\
    rm -rf /tmp/* && \\
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \\
    && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
### END CUDA BASE ###
"""
    # runtime
    ret += f"""\
### CUDA RUNTIME ###
# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/{CUDA_VERSION}/ubuntu2004/runtime/Dockerfile
ENV NCCL_VERSION {NCCL_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \\
    cuda-libraries-{CUDA_HYPHEN}={NV_CUDA_LIB_VERSION} \\
    {NV_LIBNPP_PACKAGE} \\
    cuda-nvtx-{CUDA_HYPHEN}={NV_NVTX_VERSION} \\
    {NV_LIBCUBLAS_PACKAGE} \\
    {NV_LIBNCCL_PACKAGE} && \\
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    apt-get clean && \\
    rm -rf $HOME/.cache/* && \\
    rm -rf /tmp/* && \\
    rm -rf /var/lib/apt/lists/*
    
# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold {NV_LIBCUBLAS_PACKAGE_NAME} {NV_LIBNCCL_PACKAGE_NAME}
### END CUDA RUNTIME ###
"""
    # devel
    ret += f"""\
### CUDA DEVEL ###
# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/{CUDA_VERSION}/ubuntu2004/devel/Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libtinfo5 libncursesw5 \\
    cuda-cudart-dev-{CUDA_HYPHEN}={NV_CUDA_CUDART_DEV_VERSION} \\
    cuda-command-line-tools-{CUDA_HYPHEN}={NV_CUDA_LIB_VERSION} \\
    cuda-minimal-build-{CUDA_HYPHEN}={NV_CUDA_LIB_VERSION} \\
    cuda-libraries-dev-{CUDA_HYPHEN}={NV_CUDA_LIB_VERSION} \\
    cuda-nvml-dev-{CUDA_HYPHEN}={NV_NVML_DEV_VERSION} \\
    {NV_LIBNPP_DEV_PACKAGE} \\
    libcusparse-dev-{CUDA_HYPHEN}={NV_LIBCUSPARSE_DEV_VERSION} \\
    {NV_LIBCUBLAS_DEV_PACKAGE} \\
    {NV_LIBNCCL_DEV_PACKAGE} && \\
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    apt-get clean && \\
    rm -rf $HOME/.cache/* && \\
    rm -rf /tmp/* && \\
    rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold {NV_LIBCUBLAS_DEV_PACKAGE_NAME} {NV_LIBNCCL_DEV_PACKAGE_NAME}

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs
### END CUDA DEVEL ###
"""
    # cudnn devel
    ret += f"""\
### CUDANN8 DEVEL ###
# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/{CUDA_VERSION}/ubuntu2004/devel/cudnn8/Dockerfile
ENV CUDNN_VERSION {NV_CUDNN_VERSION}
LABEL com.nvidia.cudnn.version="{NV_CUDNN_VERSION}"
RUN apt-get update && apt-get install -y --no-install-recommends \\
    {NV_CUDNN_PACKAGE} \\
    {NV_CUDNN_PACKAGE_DEV} \\
    && apt-mark hold {NV_CUDNN_PACKAGE_NAME} && \\
    # Cleanup
    apt-get clean && \\
    rm -rf /root/.cache/* && \\
    rm -rf /tmp/* && \\
    rm -rf /var/lib/apt/lists/*

### END CUDANN8 ###
"""
    # Cupti
    ret += """\
# Link Cupti:
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/cuda/extras/CUPTI/lib64
"""
    return ret


def python_string(miniconda_version: str, python_version: str) -> str:
    major_version, minor_version = python_version.split('.')

    MINICONDA_VERSION = miniconda_version
    MINICONDA_MD5 = MINICONDA_INFO_DICT[MINICONDA_VERSION][f'{major_version}{minor_version}']

    return f"""\
### RUNTIMES ###
# Install Miniconda: https://repo.continuum.io/miniconda/
ENV \\
    # TODO: CONDA_DIR is deprecated and should be removed in the future
    CONDA_DIR=/opt/conda \\
    CONDA_ROOT=/opt/conda \\
    PYTHON_VERSION="{python_version}" \\
    CONDA_PYTHON_DIR=/opt/conda/lib/python{python_version} \\
    MINICONDA_VERSION={MINICONDA_VERSION} \\
    MINICONDA_MD5={MINICONDA_MD5} \\
    CONDA_VERSION={MINICONDA_VERSION}

RUN wget --no-verbose https://repo.anaconda.com/miniconda/Miniconda3-py3{minor_version}_{MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \\
    echo "${{MINICONDA_MD5}} *miniconda.sh" | md5sum -c - && \\
    /bin/bash ~/miniconda.sh -b -p $CONDA_ROOT && \\
    export PATH=$CONDA_ROOT/bin:$PATH && \\
    rm ~/miniconda.sh && \\
    # Configure conda
    # TODO: Add conde-forge as main channel -> remove if testted
    # TODO, use condarc file
    $CONDA_ROOT/bin/conda config --system --add channels conda-forge && \\
    $CONDA_ROOT/bin/conda config --system --set auto_update_conda False && \\
    $CONDA_ROOT/bin/conda config --system --set show_channel_urls True && \\
    $CONDA_ROOT/bin/conda config --system --set channel_priority strict && \\
    # Deactivate pip interoperability (currently default), otherwise conda tries to uninstall pip packages
    $CONDA_ROOT/bin/conda config --system --set pip_interop_enabled false && \\
    # Update conda
    $CONDA_ROOT/bin/conda update -y -n base -c defaults conda && \\
    $CONDA_ROOT/bin/conda update -y setuptools && \\
    $CONDA_ROOT/bin/conda install -y conda-build && \\
    $CONDA_ROOT/bin/conda install -y --update-all python=$PYTHON_VERSION && \\
    # Link Conda
    ln -s $CONDA_ROOT/bin/python /usr/local/bin/python && \\
    ln -s $CONDA_ROOT/bin/conda /usr/bin/conda && \\
    # Update
    $CONDA_ROOT/bin/conda install -y pip && \\
    $CONDA_ROOT/bin/pip install --upgrade pip && \\
    chmod -R a+rwx /usr/local/bin/ && \\
    # Cleanup - Remove all here since conda is not in path as of now
    # find /opt/conda/ -follow -type f -name '*.a' -delete && \\
    # find /opt/conda/ -follow -type f -name '*.js.map' -delete && \\
    $CONDA_ROOT/bin/conda clean -y --packages && \\
    $CONDA_ROOT/bin/conda clean -y -a -f  && \\
    $CONDA_ROOT/bin/conda build purge-all && \\
    # Fix permissions
    fix-permissions.sh $CONDA_ROOT && \\
    clean-layer.sh

ENV PATH=$CONDA_ROOT/bin:$PATH

### END RUNTIMES ###
"""


def dev_tools() -> str:
    return """\
### DEV TOOLS ###

## Install Jupyter Notebook
RUN \\
    pip install notebook voila ipywidgets jupyter_contrib_nbextensions autopep8 yapf && \\
    # Activate and configure extensions
    jupyter contrib nbextension install --sys-prefix && \\
    clean-layer.sh

## For Notebook Branding
COPY branding/logo.png /tmp/logo.png
COPY branding/favicon.ico /tmp/favicon.ico
RUN /bin/bash -c 'cp /tmp/logo.png $(python -c "import sys; print(sys.path[-1])")/notebook/static/base/images/logo.png'
RUN /bin/bash -c 'cp /tmp/favicon.ico $(python -c "import sys; print(sys.path[-1])")/notebook/static/base/images/favicon.ico'
RUN /bin/bash -c 'cp /tmp/favicon.ico $(python -c "import sys; print(sys.path[-1])")/notebook/static/favicon.ico'

## Install Visual Studio Code Server
RUN curl -fsSL https://code-server.dev/install.sh | sh && \\
    clean-layer.sh

## Install ttyd. (Not recommended to edit)
RUN \\
    wget https://github.com/tsl0922/ttyd/archive/refs/tags/1.6.2.zip \\
    && unzip 1.6.2.zip \\
    && cd ttyd-1.6.2 \\
    && mkdir build \\ 
    && cd build \\
    && cmake .. \\
    && make \\
    && make install

### END DEV TOOLS ###

# Make folders
ENV WORKSPACE_HOME="/workspace"
RUN \\
    if [ -e $WORKSPACE_HOME ] ; then \\
    chmod a+rwx $WORKSPACE_HOME; \\   
    else \\
    mkdir $WORKSPACE_HOME && chmod a+rwx $WORKSPACE_HOME; \\
    fi
ENV HOME=$WORKSPACE_HOME
WORKDIR $WORKSPACE_HOME
"""


def main(args: Namespace):
    dockerfile = ''
    # Basics
    dockerfile += basic_string()
    # CUDA
    dockerfile += cuda_string(args.cuda_version)
    # Python
    dockerfile += python_string(args.miniconda_version, args.python_version)
    # Dev Tools
    dockerfile += dev_tools()
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)


if __name__ == '__main__':
    args = define_arg_parser()
    main(args)
