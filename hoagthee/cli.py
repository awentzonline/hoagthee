#!/usr/bin/env python
from argparse import ArgumentParser
import os
import sys
import yaml

from rtmbot import RtmBot


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


def main(args=None):
    # load args with config path if not specified
    if not args:
        args = parse_args()

    config = yaml.load(open(args.config or 'rtmbot.conf', 'r'))
    config['SLACK_TOKEN'] = os.environ['SLACK_TOKEN']
    bot = RtmBot(config)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
