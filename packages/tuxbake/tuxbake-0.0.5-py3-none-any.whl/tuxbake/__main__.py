#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import sys
import json

from tuxbake.argparse import setup_parser
from tuxbake.build import build
from tuxmake.runtime import Terminated
from tuxbake.exceptions import (
    TuxbakeParsingError,
    TuxbakeRunCmdError,
)

##############
# Entrypoint #
##############
def main() -> int:
    # Parse command line
    parser = setup_parser()
    options = parser.parse_args()
    with open(options.build_definition) as reader:
        try:
            build(
                **(json.load(reader)),
                src_dir=options.src_dir,
                build_dir=options.build_dir_name,
                local_manifest=options.local_manifest,
                pinned_manifest=options.pinned_manifest,
                runtime=options.runtime,
                image=options.image,
                debug=options.debug,
                build_only=options.build_only,
                sync_only=options.sync_only,
            )
        except (KeyboardInterrupt, Terminated) as ex:
            print("tuxbake Interrupted")
        except (TuxbakeParsingError, TuxbakeRunCmdError) as ex:
            sys.stderr.write(f"{str(ex)}\n")
            sys.exit(1)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()
