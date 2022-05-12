import argparse
import json

from argparse import Namespace
from subprocess import Popen

import dockerstrings
from enums import PythonVersionEnum

CUDA_INFO_DICT = {}

def init_json():
    global CUDA_INFO_DICT
    with open('./jsons/cuda.json', 'r') as f:
        CUDA_INFO_DICT = json.load(f)


def define_arg_parser() -> Namespace:
    init_json()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cuda_version",
        choices=list(CUDA_INFO_DICT.keys()),
        default="11.3.1",
        help="cuda version"
    )
    parser.add_argument(
        "--python_version",
        default=PythonVersionEnum.DEFAULT.value,
        choices=[each.value for each in PythonVersionEnum],
        help="python version"
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="build and push docker"
    )
    parser.add_argument(
        "--tag_name",
        default="",
        help="image tag"
    )
    return parser.parse_args()


def main(args: Namespace):
    dockerfile = ""
    # Basics
    dockerfile += dockerstrings.basic
    # Ubuntu Package
    dockerfile += dockerstrings.ubuntu_package
    # CUDA
    cuda_json = CUDA_INFO_DICT[args.cuda_version]
    dockerfile += dockerstrings.cuda.format(
        CUDA_DOT_VERSION=cuda_json["CUDA_DOT_VERSION"],
        CUDA_HYPHEN_VERSION=cuda_json["CUDA_HYPHEN_VERSION"],
        CUDA_VERSION=cuda_json["CUDA_VERSION"],
        NV_CUDA_CUDART_VERSION=cuda_json["NV_CUDA_CUDART_VERSION"],
        NV_CUDA_COMPAT_PACKAGE=cuda_json["NV_CUDA_COMPAT_PACKAGE"],
        NV_CUDA_LIB_VERSION=cuda_json["NV_CUDA_LIB_VERSION"],
        NV_NVTX_VERSION=cuda_json["NV_NVTX_VERSION"],
        NV_LIBNPP_VERSION=cuda_json["NV_LIBNPP_VERSION"],
        NV_LIBCUSPARSE_VERSION=cuda_json["NV_LIBCUSPARSE_VERSION"],
        NV_LIBCUBLAS_PACKAGE_NAME=cuda_json["NV_LIBCUBLAS_PACKAGE_NAME"],
        NV_LIBCUBLAS_VERSION=cuda_json["NV_LIBCUBLAS_VERSION"],
        NV_LIBNCCL_PACKAGE_NAME=cuda_json["NV_LIBNCCL_PACKAGE_NAME"],
        NV_LIBNCCL_PACKAGE_VERSION=cuda_json["NV_LIBNCCL_PACKAGE_VERSION"],
        NCCL_VERSION=cuda_json["NCCL_VERSION"],
        NV_CUDA_CUDART_DEV_VERSION=cuda_json["NV_CUDA_CUDART_DEV_VERSION"],
        NV_NVML_DEV_VERSION=cuda_json["NV_NVML_DEV_VERSION"],
        NV_LIBCUSPARSE_DEV_VERSION=cuda_json["NV_LIBCUSPARSE_DEV_VERSION"],
        NV_LIBNPP_DEV_VERSION=cuda_json["NV_LIBNPP_DEV_VERSION"],
        NV_LIBCUBLAS_DEV_VERSION=cuda_json["NV_LIBCUBLAS_DEV_VERSION"],
        NV_LIBCUBLAS_DEV_PACKAGE_NAME=cuda_json["NV_LIBCUBLAS_DEV_PACKAGE_NAME"],
        NV_LIBNCCL_DEV_PACKAGE_NAME=cuda_json["NV_LIBNCCL_DEV_PACKAGE_NAME"],
        NV_LIBNCCL_DEV_PACKAGE_VERSION=cuda_json["NV_LIBNCCL_DEV_PACKAGE_VERSION"],
        NV_CUDNN_VERSION=cuda_json["NV_CUDNN_VERSION"],
        NV_CUDNN_PACKAGE_NAME=cuda_json["NV_CUDNN_PACKAGE_NAME"],
    )
    # Python Mamba
    dockerfile += dockerstrings.python_mamba.format(PYTHON_VERSION=args.python_version)
    # Dev Tools
    dockerfile += dockerstrings.dev_tools
    # Start shell
    dockerfile += dockerstrings.start_shell
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    if args.docker:
        if not args.tag_name:
            print('[ERROR]: tag name is need')
            exit(1)
        build_command = f"docker build -t {args.tag_name} ."
        build_flag = False
        print('Build :', build_command)
        with Popen(build_command, shell=True) as p:
            try:
                p.wait()
                build_flag = True
            except:
                p.kill()
                p.wait()

        if build_flag:
            push_command = f"docker push {args.tag_name}"
            print('Push :', push_command)
            with Popen(push_command, shell=True) as p:
                try:
                    p.wait()
                except:
                    p.kill()
                    p.wait()


if __name__ == '__main__':
    args = define_arg_parser()
    main(args)
