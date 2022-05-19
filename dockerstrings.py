basic = """\
FROM ubuntu:20.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
USER root

ENV \\
    NB_USER=root \\
    SHELL=/bin/bash \\
    HOME="/${NB_USER}" \\
    USER_GID=0 \\
    DISPLAY=:1 \\
    TERM=xterm \\
    WORKSPACE_HOME=/workspace

# Copy a script that we will use to correct permissions after running certain commands
COPY scripts/clean-layer.sh  /usr/bin/clean-layer.sh
COPY scripts/fix-permissions.sh  /usr/bin/fix-permissions.sh
RUN \\
    chmod a+rwx /usr/bin/clean-layer.sh && \\
    chmod a+rwx /usr/bin/fix-permissions.sh
"""

ubuntu_package = """\
# Install Ubuntu Package
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \\
    apt-get upgrade --yes && \\
    apt-get install --yes --no-install-recommends \\
	apt-utils \\
	autoconf \\
	automake \\
	ca-certificates \\
	cmake \\
	curl \\
	fonts-liberation \\
	g++ \\
	git \\
	gnupg2 \\
	libjson-c-dev \\
	libssl-dev \\
	libtool \\
	libwebsockets-dev \\
	locales \\
	make \\
	openssh-client \\
	openssh-server \\
	pandoc \\
	pkg-config \\
	run-one \\
	sudo \\
	tini \\
	unzip \\
	vim \\
	vim-common \\
	wget && \\
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \\
    locale-gen && \\
    clean-layer.sh

ENV \\
    LC_ALL=en_US.UTF-8 \\
    LANG=en_US.UTF-8 \\
    LANGUAGE=en_US.UTF-8
"""

cuda = """\
# Instal CUDA Package
## CUDA Base
# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/{CUDA_VERSION}/ubuntu2004/base/Dockerfile
ENV NVARCH x86_64
ENV NV_CUDA_CUDART_VERSION {NV_CUDA_CUDART_VERSION}
ENV NV_CUDA_COMPAT_PACKAGE {NV_CUDA_COMPAT_PACKAGE}

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gnupg2 curl ca-certificates && \\
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${{NVARCH}}/3bf863cc.pub | apt-key add - && \\
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${{NVARCH}} /" > /etc/apt/sources.list.d/cuda.list && \\
    rm -rf /var/lib/apt/lists/*
    
ENV CUDA_VERSION {CUDA_VERSION}

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \\
    cuda-cudart-{CUDA_DOT_VERSION}=${{NV_CUDA_CUDART_VERSION}} \\
    ${{NV_CUDA_COMPAT_PACKAGE}} \\
    && ln -s cuda-{CUDA_DOT_VERSION} /usr/local/cuda && \\
    rm -rf /var/lib/apt/lists/*
    
# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \\
    && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${{PATH}}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

## CUDA RUNTIME
ENV NV_CUDA_LIB_VERSION {NV_CUDA_LIB_VERSION}
ENV NV_NVTX_VERSION {NV_NVTX_VERSION}
ENV NV_LIBNPP_VERSION {NV_LIBNPP_VERSION}
ENV NV_LIBNPP_PACKAGE libnpp-{CUDA_HYPHEN_VERSION}=${{NV_LIBNPP_VERSION}}
ENV NV_LIBCUSPARSE_VERSION {NV_LIBCUSPARSE_VERSION}

ENV NV_LIBCUBLAS_PACKAGE_NAME {NV_LIBCUBLAS_PACKAGE_NAME}
ENV NV_LIBCUBLAS_VERSION {NV_LIBCUBLAS_VERSION}
ENV NV_LIBCUBLAS_PACKAGE ${{NV_LIBCUBLAS_PACKAGE_NAME}}=${{NV_LIBCUBLAS_VERSION}}

ENV NV_LIBNCCL_PACKAGE_NAME {NV_LIBNCCL_PACKAGE_NAME}
ENV NV_LIBNCCL_PACKAGE_VERSION {NV_LIBNCCL_PACKAGE_VERSION}
ENV NCCL_VERSION {NCCL_VERSION}
ENV NV_LIBNCCL_PACKAGE ${{NV_LIBNCCL_PACKAGE_NAME}}=${{NV_LIBNCCL_PACKAGE_VERSION}}+cuda{CUDA_DOT_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \\
    cuda-libraries-{CUDA_HYPHEN_VERSION}=${{NV_CUDA_LIB_VERSION}} \\
    ${{NV_LIBNPP_PACKAGE}} \\
    cuda-nvtx-{CUDA_HYPHEN_VERSION}=${{NV_NVTX_VERSION}} \\
    libcusparse-{CUDA_HYPHEN_VERSION}=${{NV_LIBCUSPARSE_VERSION}} \\
    ${{NV_LIBCUBLAS_PACKAGE}} \\
    ${{NV_LIBNCCL_PACKAGE}} \\
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${{NV_LIBCUBLAS_PACKAGE_NAME}} ${{NV_LIBNCCL_PACKAGE_NAME}}

## CUDA DEVEL
ENV NV_CUDA_LIB_VERSION \"{NV_CUDA_LIB_VERSION}\"

ENV NV_CUDA_CUDART_DEV_VERSION {NV_CUDA_CUDART_DEV_VERSION}
ENV NV_NVML_DEV_VERSION {NV_NVML_DEV_VERSION}
ENV NV_LIBCUSPARSE_DEV_VERSION {NV_LIBCUSPARSE_DEV_VERSION}
ENV NV_LIBNPP_DEV_VERSION {NV_LIBNPP_DEV_VERSION}
ENV NV_LIBNPP_DEV_PACKAGE libnpp-dev-{CUDA_HYPHEN_VERSION}=${{NV_LIBNPP_DEV_VERSION}}

ENV NV_LIBCUBLAS_DEV_VERSION {NV_LIBCUBLAS_DEV_VERSION}
ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME {NV_LIBCUBLAS_DEV_PACKAGE_NAME}
ENV NV_LIBCUBLAS_DEV_PACKAGE ${{NV_LIBCUBLAS_DEV_PACKAGE_NAME}}=${{NV_LIBCUBLAS_DEV_VERSION}}

ENV NV_LIBNCCL_DEV_PACKAGE_NAME {NV_LIBNCCL_DEV_PACKAGE_NAME}
ENV NV_LIBNCCL_DEV_PACKAGE_VERSION {NV_LIBNCCL_DEV_PACKAGE_VERSION}
ENV NCCL_VERSION {NCCL_VERSION}
ENV NV_LIBNCCL_DEV_PACKAGE ${{NV_LIBNCCL_DEV_PACKAGE_NAME}}=${{NV_LIBNCCL_DEV_PACKAGE_VERSION}}+cuda{CUDA_DOT_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \\
    libtinfo5 libncursesw5 \\
    cuda-cudart-dev-{CUDA_HYPHEN_VERSION}=${{NV_CUDA_CUDART_DEV_VERSION}} \\
    cuda-command-line-tools-{CUDA_HYPHEN_VERSION}=${{NV_CUDA_LIB_VERSION}} \\
    cuda-minimal-build-{CUDA_HYPHEN_VERSION}=${{NV_CUDA_LIB_VERSION}} \\
    cuda-libraries-dev-{CUDA_HYPHEN_VERSION}=${{NV_CUDA_LIB_VERSION}} \\
    cuda-nvml-dev-{CUDA_HYPHEN_VERSION}=${{NV_NVML_DEV_VERSION}} \\
    ${{NV_LIBNPP_DEV_PACKAGE}} \\
    libcusparse-dev-{CUDA_HYPHEN_VERSION}=${{NV_LIBCUSPARSE_DEV_VERSION}} \\
    ${{NV_LIBCUBLAS_DEV_PACKAGE}} \\
    ${{NV_LIBNCCL_DEV_PACKAGE}} \\
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${{NV_LIBCUBLAS_DEV_PACKAGE_NAME}} ${{NV_LIBNCCL_DEV_PACKAGE_NAME}}

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs

## CUDA DEVEL CUDNN8
ENV NV_CUDNN_VERSION {NV_CUDNN_VERSION}

ENV NV_CUDNN_PACKAGE \"libcudnn8=$NV_CUDNN_VERSION-1+cuda{CUDA_DOT_VERSION}\"
ENV NV_CUDNN_PACKAGE_DEV \"libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda{CUDA_DOT_VERSION}\"
ENV NV_CUDNN_PACKAGE_NAME \"libcudnn8\"

RUN apt-get update && apt-get install -y --no-install-recommends \\
    ${{NV_CUDNN_PACKAGE}} \\
    ${{NV_CUDNN_PACKAGE_DEV}} \\
    && apt-mark hold ${{NV_CUDNN_PACKAGE_NAME}} && \\
    rm -rf /var/lib/apt/lists/*
"""

python_mamba = """
# Install Python (mamba)
ENV \\
    CONDA_DIR=/opt/conda \\
    CONDA_ROOT=/opt/conda
ENV PATH="${{CONDA_DIR}}/bin:${{PATH}}"
ENV \\
    PYTHON_VERSION={PYTHON_VERSION} \\
    CONDA_MIRROR=https://github.com/conda-forge/miniforge/releases/latest/download

RUN set -x && \\
    # Miniforge installer
    miniforge_arch=$(uname -m) && \\
    miniforge_installer="Mambaforge-Linux-${{miniforge_arch}}.sh" && \\
    wget --quiet "${{CONDA_MIRROR}}/${{miniforge_installer}}" && \\
    /bin/bash "${{miniforge_installer}}" -f -b -p "${{CONDA_DIR}}" && \\
    rm "${{miniforge_installer}}" && \\
    # Conda configuration see https://conda.io/projects/conda/en/latest/configuration.html
    conda config --system --set auto_update_conda false && \\
    conda config --system --set show_channel_urls true && \\
    if [[ "${{PYTHON_VERSION}}" != "default" ]]; then mamba install --quiet --yes python="${{PYTHON_VERSION}}"; fi && \\
    # Pin major.minor version of python
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${{CONDA_DIR}}/conda-meta/pinned" && \\
    # Using conda to update all packages: https://github.com/mamba-org/mamba/issues/1092
    conda install -y conda-build && \\
    conda update --all --quiet --yes && \\
    conda clean --all -f -y && \\
    fix-permissions.sh $CONDA_ROOT && \\
    clean-layer.sh
"""

dev_tools = """\
# Install Dev Tools

## Install Jupyter
RUN mamba install --quiet --yes \\
    notebook \\
    jupyterhub \\
    jupyterlab \\
    voila \\
    jupyter_contrib_nbextensions \\
    ipywidgets \\
    autopep8 \\
    yapf && \\
    mamba clean --all -f -y && \\
    npm cache clean --force && \\
    jupyter contrib nbextension install --sys-prefix && \\
    fix-permissions.sh $CONDA_ROOT && \\
    clean-layer.sh
    
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

## Install ssh. (Not recommended to edit)

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

start_shell = """\
### Start Ainize Worksapce ###
COPY start.sh /scripts/start.sh
RUN ["chmod", "+x", "/scripts/start.sh"]
CMD "/scripts/start.sh"
"""