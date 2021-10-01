# -*- coding: utf-8 -*-

import os
import logging
import subprocess


# define logger
logger = logging.getLogger(__name__)
# root directory is the output if --output is not given
root = os.path.dirname(os.path.abspath(__file__))


def download(output, username=None, password=None):
    """
    Executes a list of commands and yield status + error
    For Docker Volume data creation only
        Download steps:
            - initialize an empty GIT repo
            - add remote from url
            - enable a sparse checkout
            - pull the master branch
    """
    url = "https://{username}:{password}@bitbucket.org/lorinivalerio/smfr_models_data.git".format(
        username=username,
        password=password
    )

    commands = [
        "/usr/bin/git init",
        "/usr/bin/git remote add origin {url}".format(url=url),
        "/usr/bin/git config core.sparsecheckout true",
        "echo 'models/*' > .git/info/sparse-checkout",
        "/usr/bin/git pull --depth 1 origin master",
    ]

    # skip git init if repo exists
    if os.path.exists(os.path.join(output, "models/current-model.json")):
        logger.debug("Repo already initialized")
        commands = commands[-1:]

    for cmd in commands:
        query = subprocess.Popen(
            cmd.split(' '),
            cwd=output,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        status, error = query.communicate()
        logger.debug(f'cmd: {cmd} - {error.decode("utf-8")} - {status.decode("utf-8")}')


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Download Floods model to a user defined directory.")
    parser.add_argument('--username', help='Bitlocker username', required=True)
    parser.add_argument('--password', help='Bitlocker password', required=True)
    parser.add_argument('-o', '--output', help='Output path', default=os.path.join(root, "model"))
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()
    # configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    # download model
    logger.info("downloading floods model...")
    download(args.output, username=args.username, password=args.password)
    logger.info(f"downloaded to {args.output}")
