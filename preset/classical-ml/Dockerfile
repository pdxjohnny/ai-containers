# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.

# based on https://github.com/pytorch/pytorch/blob/master/Dockerfile
#
# NOTE: To build this you will need a docker version >= 19.03 and DOCKER_BUILDKIT=1
#
#       If you do not use buildkit you are not going to have a good time
#
#       For reference:
#           https://docs.docker.com/develop/develop-images/build_enhancements/

ARG BASE_IMAGE="ubuntu"
ARG BASE_TAG="22.04"

FROM ${BASE_IMAGE}:${BASE_TAG} as classical-ml-base

ENV DEBIAN_FRONTEND=noninteractive

# See http://bugs.python.org/issue19846

ENV LANG=C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    bzip2 \
    ca-certificates \
    diffutils \
    gcc \
    git \
    gzip \
    make \
    patch \
    rsync \
    unzip \
    wget \
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

FROM classical-ml-base as classical-ml-python

# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash -m dev
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda
ARG MINICONDA_VERSION
ARG PYTHON_VERSION
ARG IDP_VERSION
ARG INTEL_CHANNEL

RUN wget --progress=dot:giga --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh -O miniconda.sh && \
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p "${CONDA_ROOT}" && \
    rm ./miniconda.sh && \
    ln -s "${CONDA_ROOT}" "${CONDA_ROOT}/../miniconda3"  && \
    export PATH="${CONDA_ROOT}/bin/:${PATH}" && \
    conda update -y conda && \
    conda config --add channels conda-forge && \
    conda config --add channels intel && \
    conda init --all && \
    conda install -c conda-forge \
        jupyterlab \
        notebook \
        jupyterhub \
        jupyter-server-proxy  && \
        jupyter labextension disable "@jupyterlab/apputils-extension:announcements" && \
    conda clean -y --all

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}

ARG IDP_VERSION
ARG DPNP_VERSION
ARG XGBOOST_VERSION
ARG MODIN_VERSION
ARG NUMPY_VERSION
ARG SKLEARNEX_VERSION

# Conda packages
RUN conda create -yn classical-ml -c ${INTEL_CHANNEL} -c conda-forge \
        dpnp=${DPNP_VERSION} \
        numpy=${NUMPY_VERSION} \
        python=${PYTHON_VERSION} \
        scikit-learn-intelex==${SKLEARNEX_VERSION} \
        xgboost=${XGBOOST_VERSION} \
        modin-ray=${MODIN_VERSION} \
        python-dotenv \
        tqdm \
        matplotlib-base \
        dataset_librarian \
        threadpoolctl \
        ipython \
        ipykernel \
        kernda \
        protobuf=4.24 \
        'pillow>=10.2.0' \
        'tornado>=6.3.3' && \
    conda clean -y --all



# PyPI packages
RUN conda run -n classical-ml python -m pip install --no-deps --no-cache-dir \
    cloud-data-connector


ENV PYTHONSTARTUP=~/.patch_sklearn.py
COPY base/.patch_sklearn.py ~/.patch_sklearn.py

ENV PYTHONSTARTUP=/home/dev/.patch_sklearn.py
COPY base/.patch_sklearn.py /home/dev/.patch_sklearn.py

FROM classical-ml-python as classical-ml-jupyter

EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

WORKDIR /home/dev
COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests

RUN "${CONDA_ROOT}/envs/classical-ml/bin/python" -m ipykernel install --user --name classical-ml --display-name "Classical ML" && \
    "${CONDA_ROOT}/envs/classical-ml/bin/kernda" -o -y "$HOME/.local/share/jupyter/kernels/$(echo classical-ml | sed -e 's/\(.*\)/\L\1/')/kernel.json" && \
    "${CONDA_ROOT}/envs/classical-ml/bin/python" -m ipykernel.kernelspec --user && \
    conda clean -y --all

CMD ["bash", "-c", "source activate classical-ml && jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate classical-ml" >> ~/.bashrc
