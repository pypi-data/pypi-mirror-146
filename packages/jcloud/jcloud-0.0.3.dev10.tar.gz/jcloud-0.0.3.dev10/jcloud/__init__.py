__version__ = '0.0.3.dev10'


def main():
    from .parsers import get_main_parser

    args = get_main_parser().parse_args()

    if args.loglevel:
        import os

        os.environ['JCLOUD_LOGLEVEL'] = args.loglevel

    try:
        from jcloud import api

        getattr(api, args.cli.replace('-', '_'))(args)
    except KeyboardInterrupt:
        pass
