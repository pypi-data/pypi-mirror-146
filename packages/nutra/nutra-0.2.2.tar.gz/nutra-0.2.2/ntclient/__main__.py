# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:02:19 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2022  Shane Jaroch <nutratracker@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
import sys
import time
from urllib.error import HTTPError, URLError

import argcomplete
from colorama import init as colorama_init

from ntclient import (
    __db_target_nt__,
    __db_target_usda__,
    __title__,
    __version__,
    set_flags,
)
from ntclient.argparser import build_subcommands
from ntclient.persistence import persistence_init
from ntclient.utils.exceptions import SqlException

colorama_init()


def build_argparser():
    """Adds all subparsers and parsing logic"""

    arg_parser = argparse.ArgumentParser(prog=__title__)
    arg_parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{0} cli version {1} ".format(__title__, __version__)
        + "[DB usda v{0}, nt v{1}]".format(__db_target_usda__, __db_target_nt__),
    )

    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="enable detailed error messages"
    )
    arg_parser.add_argument(
        "--no-pager",
        dest="no_paging",
        action="store_true",
        help="disable paging (print full output)",
    )

    # Subparsers
    subparsers = arg_parser.add_subparsers(title="%s subcommands" % __title__)
    build_subcommands(subparsers)

    return arg_parser


def main(args=None):
    """Main method for CLI"""

    start_time = time.time()
    arg_parser = build_argparser()
    argcomplete.autocomplete(arg_parser)

    def parse_args():
        if args is None:
            return arg_parser.parse_args()
        return arg_parser.parse_args(args=args)

    def func():
        if hasattr(args, "func"):
            persistence_init()
            args_dict = dict(vars(args))
            for expected_arg in ["func", "debug", "no_paging"]:
                args_dict.pop(expected_arg)
            # Run function
            if args_dict:
                return args.func(args=args)
            return args.func()
        return 1, arg_parser.print_help()

    args = parse_args()
    set_flags(args)
    from ntclient import DEBUG  # pylint: disable=import-outside-toplevel

    exit_code = None
    try:
        exit_code, *_results = func()
        return exit_code
    except SqlException as sql_exception:
        print("Issue with an sqlite database: " + repr(sql_exception))
        if DEBUG:
            raise
    except HTTPError as http_error:
        err_msg = "{0}: {1}".format(http_error.code, repr(http_error))
        print("Server response error, try again: " + err_msg)
        if DEBUG:
            raise
    except URLError as url_error:
        print("Connection error, check your internet: " + url_error.reason)
        if DEBUG:
            raise
    except Exception as exception:  # pylint: disable=broad-except
        print("There was an unforeseen error: " + repr(exception))
        if DEBUG:
            raise
    finally:
        if DEBUG:
            exc_time = time.time() - start_time
            print("\nExecuted in: %s ms" % round(exc_time * 1000, 1))
            print("Exit code: %s" % exit_code)


if __name__ == "__main__":
    sys.exit(main())
