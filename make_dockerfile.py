import argparse
import json

from argparse import Namespace
from subprocess import Popen

import dockerstrings

CUDA_INFO_DICT = {}
MINICONDA_INFO_DICT = {}


def init_json():
    global CUDA_INFO_DICT, MINICONDA_INFO_DICT
    with open('./jsons/cuda.json', 'r') as f:
        CUDA_INFO_DICT = json.load(f)
    with open('./jsons/miniconda.json', 'r') as f:
        MINICONDA_INFO_DICT = json.load(f)


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
    # Miniconda
    miniconda_json = MINICONDA_INFO_DICT[args.miniconda_version]
    python_version_info = args.python_version.split('.')
    python_info = f'{python_version_info[0]}{python_version_info[1]}'
    dockerfile += dockerstrings.miniconda.format(
        PYTHON_INFO=python_info,
        PYTHON_VERSION=args.python_version,
        MINICONDA_VERSION=args.miniconda_version,
        MINICONDA_MD5=miniconda_json[python_info],
    )
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
