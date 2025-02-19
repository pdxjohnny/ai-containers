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


# This image provides a Python 3.9 environment you can use to run your Python
# applications.

ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}-dl-base as inference-optimization

ENV SIGOPT_PROJECT=.

ARG NEURAL_COMPRESSOR_VERSION
ARG INTEL_CHANNEL


RUN conda install -yn pytorch-cpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda install -yn pytorch-gpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda install -yn tensorflow-cpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda install -yn tensorflow-gpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda run -n tensorflow-cpu python -m pip install --no-deps --no-cache-dir \
        tf2onnx \
        onnxruntime && \
    conda clean -y --all

RUN conda run -n tensorflow-gpu python -m pip install --no-deps --no-cache-dir \
        tf2onnx \
        onnxruntime && \
    conda clean -y --all

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests
