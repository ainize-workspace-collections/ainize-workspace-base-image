## ainize-workspace-base-image
This project is to create a Base Image for use in [Ainize Workspace](https://ainize.ai/workspace).  

### How to Use
```shell
python make_dockerfile.py
```

### Image
| os           | python | cuda   | image                                                                                |
|--------------|--------|--------|--------------------------------------------------------------------------------------|
| ubuntu 20.04 | 3.9    | 11.3.1 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.3.1-py3.9-dev) |
| ubuntu 20.04 | 3.9    | 11.2.2 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.2.2-py3.9-dev) |
| ubuntu 20.04 | 3.9    | 11.1.1 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.1.1-py3.9-dev) |
| ubuntu 20.04 | 3.9    | 11.0.3 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.0.3-py3.9-dev) |
| ubuntu 20.04 | 3.8    | 11.3.1 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.3.1-py3.8-dev) |
| ubuntu 20.04 | 3.8    | 11.2.2 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.2.2-py3.8-dev) |
| ubuntu 20.04 | 3.8    | 11.1.1 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.1.1-py3.8-dev) |
| ubuntu 20.04 | 3.8    | 11.0.3 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.0.3-py3.8-dev) |
| ubuntu 20.04 | 3.7    | 11.3.1 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.3.1-py3.7-dev) |
| ubuntu 20.04 | 3.7    | 11.2.2 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.2.2-py3.7-dev) |
| ubuntu 20.04 | 3.7    | 11.1.1 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.1.1-py3.7-dev) |
| ubuntu 20.04 | 3.7    | 11.0.3 | [link](https://hub.docker.com/r/byeongal/ainize-workspace-base-cuda11.0.3-py3.7-dev) |

### Reference
#### Dockerfile
- https://gitlab.com/nvidia/container-images/cuda
- https://github.com/ml-tooling/ml-workspace/
- https://github.com/pytorch/pytorch/blob/master/Dockerfile
- https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/dockerfiles/dockerfiles
#### Software
- https://repo.anaconda.com/miniconda/
- https://jupyter.org/
- https://github.com/tsl0922/ttyd
- https://github.com/coder/code-server
