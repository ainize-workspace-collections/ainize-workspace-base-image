import argparse
import json

from argparse import Namespace
from subprocess import Popen

import dockerstrings
from enums import PythonVersionEnum

CUDA_INFO_DICT = {}


def init_json():
    global CUDA_INFO_DICT
    with open("./jsons/cuda.json", "r") as f:
        CUDA_INFO_DICT = json.load(f)


def define_arg_parser() -> Namespace:
    init_json()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--os",
        default="ubuntu20.04",
        choices=["ubuntu18.04", "ubuntu20.04"],
    )
    parser.add_argument(
        "--cuda_version",
        default="11.3.1",
        help="cuda version",
    )
    parser.add_argument(
        "--cudnn_version",
        default="8",
        help="cudnn version",
    )
    parser.add_argument(
        "--python_version",
        default=PythonVersionEnum.DEFAULT.value,
        choices=[each.value for each in PythonVersionEnum],
        help="python version",
    )
    parser.add_argument("--docker", action="store_true", help="build and push docker")
    parser.add_argument("--tag_name", default="", help="image tag")
    return parser.parse_args()


def main(args: Namespace):
    dockerfile = ""
    # Basics
    if args.cuda_version in CUDA_INFO_DICT[args.os][f"cudnn{args.cudnn_version}"]:
        os_info = args.os
        cudnn_info = f"cudnn{args.cudnn_version}"
        cuda_info = args.cuda_version
        dockerfile += dockerstrings.basic.format(
            DOCKER_BASE_IMAGE=f"{cuda_info}-{cudnn_info}-devel-{os_info}"
        )
    else:
        # Only Support Ubuntu
        os_info = args.os[:6] + ":" + args.os[6:]
        dockerfile += dockerstrings.basic.format(
            DOCKER_BASE_IMAGE=os_info
        )
        
    # Ubuntu Package
    dockerfile += dockerstrings.ubuntu_package
    # Python Mamba
    dockerfile += dockerstrings.python_mamba.format(PYTHON_VERSION=args.python_version)
    # Dev Tools
    dockerfile += dockerstrings.dev_tools
    # Start shell
    dockerfile += dockerstrings.start_shell
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)
    if args.docker:
        if not args.tag_name:
            print("[ERROR]: tag name is need")
            exit(1)
        build_command = f"docker build -t {args.tag_name} ."
        build_flag = False
        print("Build :", build_command)
        with Popen(build_command, shell=True) as p:
            try:
                p.wait()
                build_flag = True
            except:
                p.kill()
                p.wait()

        if build_flag:
            push_command = f"docker push {args.tag_name}"
            print("Push :", push_command)
            with Popen(push_command, shell=True) as p:
                try:
                    p.wait()
                except:
                    p.kill()
                    p.wait()


if __name__ == "__main__":
    args = define_arg_parser()
    main(args)
