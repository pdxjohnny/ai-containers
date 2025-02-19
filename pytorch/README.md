# PyTorch Ingredients

## PyTorch

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IDP_VERSION | `core` | Intel Distribution of Python version(either `full` or `core`) |
| IPEX_VERSION | `2.2.0` | Intel Extension for PyTorch Version |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| PYTORCH_VERSION | `2.2.0+cpu` | PyTorch Version |
| TORCHAUDIO_VERSION | `2.2.0+cpu` | TorchAudio Version |
| TORCHVISION_VERSION | `0.17.0+cpu` | TorchVision Version |

### Jupyter

### MultiNode

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| INC_VERSION | `2.4.1` | Neural Compressor Version |
| ONECCL_VERSION | `2.2.0+cpu` | TorchCCL Version |

### XPU Base

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| ICD_VER | `23.43.27642.40-803~22.04` | OpenCL Version |
| LEVEL_ZERO_GPU_VER | `1.3.27642.40-803~22.04` | Level Zero GPU Version |
| LEVEL_ZERO_VER | `1.14.0-744~22.04` | Level Zero Version |
| LEVEL_ZERO_DEV_VER | `1.14.0-744~22.04` | Level Zero Dev Version |
| DPCPP_VER | `2024.1.0-963` | DPCPP Version |
| MKL Version | `2024.1.0-691` | MKL Version |
| CCL_VER | `2021.12.0-309` | CCL Version |
| PYTORCH_XPU_VERSION | `2.1.0a0+cxx11.abi` | Torch Version |
| TORCHVISION_XPU_VERSION | `0.16.0.post0+cxx11.abi` | Torchvision Version |
| TORCHAUDIO_XPU_VERSION | `2.1.0.post0+cxx11.abi` | Torchaudio Version |
| IPEX_XPU_VERSION | `2.1.20+xpu` | IPEX Version |
| ONECCL_VERSION | `2.1.200` | TorchCCL Version |

### XPU Jupyter

## TorchServe

## Distributed Training on k8s

Use _N_-Nodes in your Training with PyTorchJobs and Kubeflow's Training Operator with an optimized production container.

### Distributed Production Container

Create a Distributed Production Container using Intel Optimized PyTorch MultiNode layers. For Example:

```dockerfile
# Add Some Multinode image layers
FROM intel/intel-optimized-pytorch:2.1.0-pip-multinode as prod-base
# Use an existing container target
FROM base as prod

# Copy in Intel Optimized PyTorch MultiNode python environment, this will overwrite any packages with the same name
COPY --from=prod-base /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=prod-base /usr/local/bin /usr/local/bin

...
```

#### Build the Container with New Stage

```bash
docker build ... --target prod -t my_container:prod .
```

### Configure Kubernetes

Using an existing Kubernetes Cluster of any flavor, install the standalone training operator from GitHub or use a pre-existing Kubeflow configuration.

```bash
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone"
```

Ensure that the training operator deployment readiness status `1/1` before proceeding.

### Deploy Distributed Job

Install [Helm](https://helm.sh/docs/intro/install/)

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
chmod 700 get_helm.sh && \
./get_helm.sh
```

Configure the Helm Chart by changing [pytorchjob](chart/templates/pytorchjob.yaml#L18-L46), [pvc](chart/templates/pvc.yaml), and [values](chart/values.yaml) files.

Afterwards, deploy to the cluster with `helm install`. To see all of the options, see the [README](chart/README.md) for the chart.

```bash
export NAMESPACE=kubeflow
helm install ---namespace ${NAMESPACE} \
     --set metadata.name=<workflow-name> \
     --set metadata.namespace=<namespace with training operator> \
     --set imageName=<Docker Image repository/Name> \
     --set imageTag=<Docker Image Tag> \
     ...
     ipex-distributed
     charts/training
```

To see an existing configuration utilizing this method, check out [Intel® Extension for Transformers](https://github.com/intel/intel-extension-for-transformers/blob/main/docker/README.md#kubernetes)' implementation.

### Troubleshooting

- [TorchCCL Reference](https://github.com/intel/torch-ccl)
- [PyTorchJob Reference](https://www.kubeflow.org/docs/components/training/pytorch/)
- [Training Operator Reference](https://github.com/kubeflow/training-operator)
- When applying proxies specify all of your proxies in a configmap in the same namespace, and add the following to both your launcher and workers:

```yaml
envFrom:
  - configMapRef:
      name: my-proxy-configmap-name
```
