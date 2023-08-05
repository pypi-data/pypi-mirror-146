import logging
import os
import shutil
from distutils.dir_util import copy_tree

import setuptools
from travel.cli.setupper import Setupper
from travel.config.reader import parse_bags
from travel.custom.tasks import performer
from travel.tools.venv import Virtualenv

logger = logging.getLogger(__name__)


def pack(context: str, command: str, target: str = None, setup: bool = True):

    # Setup the bags and dependencies
    if setup:
        current_bag, all_bags = Setupper().manage(context, target=target)
    else:
        current_bag, all_bags = parse_bags(context, target)
        Virtualenv(current_bag).create()

    # Pre-pack
    performer.perform_tasks("pack", "pre", current_bag)

    # Get the right python (this might be useful in case the setup.py uses a particular syntax)
    env = Virtualenv(current_bag)

    # Clean the previous target folder, if existing
    build_folder = current_bag.build_folder
    if os.path.isdir(build_folder):
        shutil.rmtree(build_folder)

    # Copy the structure of this package
    _copy_folder(current_bag.setup_py_folder, build_folder)
    source_build_folder = os.path.join(build_folder, os.path.basename(current_bag.setup_py_folder))
    # For all dependencies, copy their code too
    for dep in current_bag.flat_dependencies():
        # For all code packages, copy it inside the copied setup.py folder
        for folder in [b for b in setuptools.find_packages(where=dep.setup_py_folder) if "." not in b]:
            _copy_folder(
                os.path.join(dep.setup_py_folder, folder),
                os.path.join(source_build_folder)
            )

    # Setup the code
    setup_py = os.path.join(source_build_folder, "setup.py")
    env.python.run(f"{setup_py} {' '.join(command)}", cwd=source_build_folder)  # TODO should check for spaces and commas, or use list!

    # Post-pack
    performer.perform_tasks("pack", "post", current_bag)


def _copy_folder(source, destination):
    os.makedirs(destination, exist_ok=True)
    right_destination = os.path.join(destination, os.path.basename(os.path.normpath(source)))
    return copy_tree(source, right_destination)
