import argparse
import logging
import os

from garden.cli import python_wrapper, blueprinter, packer
from garden.cli.cleaner import Cleaner
from garden.cli.setupper import Setupper

logger = logging.getLogger(__name__)


def main():

    # Garden
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", default=os.getcwd(), help="Path to the folder containing the nest.yml file")
    parser.set_defaults(action=lambda args: parser.parse_args(["-h"]))
    subparsers = parser.add_subparsers()

    # Clean
    clean = subparsers.add_parser("clean")
    clean.set_defaults(action=lambda args, rest: Cleaner().manage(args.context))

    # Blueprint
    blueprint = subparsers.add_parser("blueprint")
    blueprint.add_argument("--local-blueprints", help="Extra folders containing the main nest.yml of the local blueprints to use", nargs="+", required=False)
    blueprint.set_defaults(action=lambda args, rest: blueprinter.run(args.context, local_blueprints=args.local_blueprints))

    # Setup
    setup = subparsers.add_parser("setup")
    setup.set_defaults(action=lambda args, rest: Setupper().manage(args.context))

    # Pack
    pack = subparsers.add_parser("pack")
    pack.add_argument("--target", help="Name of the nest to run setup.py commands", required=False)
    pack.add_argument("--no-setup", help="Do not update the venvs", required=False, action="store_true")
    pack.set_defaults(action=lambda args, rest: packer.pack(args.context, rest, target=args.target, setup=not args.no_setup))

    # Release

    # # Python
    # python = subparsers.add_parser("python")
    # python.add_argument("package", help="Name of the nest (it will be used to activate its venv)")
    # python.set_defaults(action=lambda args, rest: python_wrapper.run(args.context, args.package, rest))

    # Parse args and invoke the corresponding functions
    arguments, remainder = parser.parse_known_args()
    arguments.action(arguments, remainder)
    logger.info("All done.")


if __name__ == '__main__':
    main()
