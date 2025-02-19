# Generic Test Runner

Test Runner is a simple automated testing framework for replicating and validating a user's command line interface experience with Intel AI Containers and Benchmarks.

## Quickstart

These steps assume you are using a modern Linux OS like [Ubuntu 22.04](https://www.releases.ubuntu.com/jammy/) with [Python 3.10+](https://www.python.org/downloads/release/python-3100/).

```bash
git clone https://github.com/intel/ai-containers
pip install -r ai-containers/test-runner/requirements.txt
touch tests.yaml
python ai-containers/test-runner/test_runner.py -f tests.yaml
```

1. Install the python requirements file
2. Create a `tests.yaml` file in your project's test directory
3. Add a [test](#test-definition) to the `tests.yaml` file
4. Run the Test Runner application command line interface to execute the test

### Test Definition

A test is defined as a set of commands to be executed along with their associated configurations. Each test is represented as an instance of the Test class, which has the following properties:

| Properties | Type           | Description  |
|------------|----------------|--------------|
| name       | str            | The name of the test. |
| cmd        | str            | The command to be executed for the test. |
| [img](https://github.com/compose-spec/compose-spec/blob/master/spec.md#image)        | Optional[str]  | The Docker image to be used when running the test in a container. |
| [volumes](https://github.com/compose-spec/compose-spec/blob/master/spec.md#volumes)    | Optional[List[[Volume](utils/test.py#L13)]] | A list of volumes to be mounted when running the test in a container. |
| [env](https://github.com/compose-spec/compose-spec/blob/master/spec.md#environment)        | Optional[Dict[str, str]] | A list of environment variables to be set when the test is running. |
| notebook   | Optional[str]  | A flag indicating whether the test utilizes a [jupyter notebook](#notebook-test). |
| serving    | Optional[str]  | A flag indicating whether a [serving test](#serving-test) should be invoked. |
| [cap_add](https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add)    | Optional[str]  | Specifies additional container capabilities. |
| [device](https://github.com/compose-spec/compose-spec/blob/master/spec.md#devices)     | Optional[str]  | Defines a list of device mappings like a dGPU. |
| [entrypoint](https://github.com/compose-spec/compose-spec/blob/master/spec.md#entrypoint) | Optional[str]  | Overrides the entrypoint for the container specified by the image. |
| [hostname](https://github.com/compose-spec/compose-spec/blob/master/spec.md#hostname)   | Optional[str]  | Declares a custom host name to use for the container. |
| [ipc](https://github.com/compose-spec/compose-spec/blob/master/spec.md#ipc)        | Optional[str]  | Configures the IPC isolation mode set by the container. |
| [privileged](https://github.com/compose-spec/compose-spec/blob/master/spec.md#privileged) | Optional[bool] | Configures the container to run with elevated privileges. |
| [pull](https://github.com/compose-spec/compose-spec/blob/master/spec.md#pull_policy)       | Optional[str]  | Defines the pull policy used by the docker API when invoking the test. |
| [user](https://github.com/compose-spec/compose-spec/blob/master/spec.md#user)       | Optional[str]  | Overrides the user used to run the container process specified by the image. |
| [shm_size](https://github.com/compose-spec/compose-spec/blob/master/spec.md#shm_size)   | Optional[str]  | Configures the size of the shared memory `/dev/shm` partition allowed by the container. |
| [workdir](https://github.com/compose-spec/compose-spec/blob/master/spec.md#working_dir)    | Optional[str]  | Overrides the container's workding directory specified by the image. |

> [!TIP]
> To find more information about each property, click on the attribute link to see it's OCI spec definition. To see the list of default values used for each property, see the [class definition](utils/test.py#L18).

### Advanced Tests

There are two more complex properties that can be enabled to provide additional functionality to your tests.

#### Notebook Test

A notebook test is a special type of test designed to run Jupyter notebooks. This is indicated by setting the notebook attribute to `True` in the test definition. When a test is marked as a notebook test, the command specified in the cmd attribute is expected to be [papermill](https://github.com/nteract/papermill) command. If papermill is not already installed in the provided `image` property, then it will be installed.

Here's an example of a notebook test definition:

```yaml
notebook_test:
  cmd: papermill --log-output my_notebook.ipynb result.ipynb
  img: jupyter/scipy-notebook:latest
  notebook: true
```

In this example, `my_notebook.ipynb` is a Jupyter notebook that will be executed as the test using the `papermill` command line interface.

#### Serving Test

A serving test is a test that involves running a server and making requests to it. This is indicated by setting the serving attribute to `True` in the test definition. When a test is marked as a serving test, the command specified in the `cmd` attribute is expected to be run by a client `python:3.11` container. The image and entrypoint specified in the `img` and `entrypoint` properties are the server image and command you are attempting to test.

Here's an example of a serving test definition:

```yaml
serving-test:
  img: nginx:latest
  cmd: bash client_rest_test.sh
  entrypoint: nginx -g daemon off;
  serving: True
```

In this example, `client_rest_test.sh` is a bash script that executes `cURL` commands to the `nginx:latest` image. The test runner will start the server, and then execute the client commands.

## Usage

This application is designed to run a series of tests defined in a YAML configuration file. These tests can be run either directly on the host system (baremetal) or within a Docker container. The application can execute one test file using the command line interface.

To run the CLI, use the following command:

```bash
python main.py -f /path/to/tests.yaml
```

The -f option is used to specify the path to the YAML file containing the test definitions.

For more options, see the `--help` output below:

```text
$ python test_runner.py --help
usage: test_runner.py [-h] [-a ACTIONS_PATH] [-f FILE_PATH] [-v] [-l LOGS_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -a ACTIONS_PATH, --actions-file ACTIONS_PATH
                        -a /path/to/.actions.json
  -f FILE_PATH, --file FILE_PATH
                        -f /path/to/tests.yaml
  -v, --verbose         DEBUG Loglevel
  -l LOGS_PATH, --logs LOGS_PATH
                        -l /path/to/logs
```

### Run Modes

There are two modes for running the tests: baremetal and container.

#### Baremetal

In baremetal mode, the test command is executed directly on the host system. This mode is used when the img attribute is not provided in the test definition.

Example of a test definition for baremetal mode:

```yaml
test1:
  cmd: echo "Hello, World!"
  env:
    VAR1: value1
    VAR2: value2
```

#### Container

In container mode, the test command is executed within a Docker container. This mode is used when the `img` attribute is provided in the test definition.

Example of a test definition for container mode:

```yaml
test2:
  cmd: echo "Hello, Docker!"
  img: ubuntu:latest
  volumes:
    - src: /host/path
      dst: /container/path
  env:
    VAR1: value1
    VAR2: value2
```

In this example, the echo command will be executed in an `ubuntu:latest` Docker container, with the `/host/path` directory on the host system mounted to `/container/path` in the container.

## GitHub Actions CI/CD

This composite action clones this repository just as in the [quickstart](#quickstart) section and runs the application on a given target `recipe_dir` directory.

Inputs for the action:

```yaml
inputs:
  mlops_repo:
    description: 'Test Runner org/repo'
    required: true
    type: string
  mlops_ref:
    description: 'Test Runner Branch/Tag'
    required: false
    default: develop
    type: string
  recipe_dir:
    description: 'Path to Recipe Directory'
    required: false
    type: string
  registry:
    description: 'Container Registry URL'
    required: true
    type: string
  test_dir:
    description: 'Directory with tests.yaml to test'
    required: true
    type: string
  token:
    required: true
    type: string
```

Example Implementation of the action:

```yaml
test-containers:
  runs-on: [ self-hosted, Linux, validation ]
  steps:
    - uses: actions/checkout@v4
    - uses: docker/login-action@v3
      with:
        registry: ${{ secrets.REGISTRY }}
        username: ${{ secrets.REGISTRY_USER }}
        password: ${{ secrets.REGISTRY_TOKEN }}
    - name: Test Container Group
      uses: intel/ai-containers/test-runner@main
      with:
        mlops_repo: intel/ai-containers
        registry: ${{ secrets.REGISTRY }}
        test_dir: /path/to/test/dir
        token: ${{ github.token }}
```
