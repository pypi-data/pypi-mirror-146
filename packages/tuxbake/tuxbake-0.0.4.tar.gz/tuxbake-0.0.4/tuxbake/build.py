#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxbake.models import OEBuild
from tuxmake.runtime import Terminated
import signal
from tuxbake.exceptions import (
    TuxbakeParsingError,
    TuxbakeRunCmdError,
)
import sys


def build(**kwargs):
    old_sigterm = signal.signal(signal.SIGTERM, Terminated.handle_signal)
    try:
        oebuild = OEBuild(**kwargs)
        oebuild.validate()
        oebuild.prepare()
        oebuild.do_build()
    except (KeyboardInterrupt, Terminated) as ex:
        print("tuxbake Interrupted")
    except (TuxbakeParsingError, TuxbakeRunCmdError) as ex:
        sys.stderr.write(f"{str(ex)}\n")
        sys.exit(1)

    oebuild.do_cleanup()
    signal.signal(signal.SIGTERM, old_sigterm)
    return oebuild
