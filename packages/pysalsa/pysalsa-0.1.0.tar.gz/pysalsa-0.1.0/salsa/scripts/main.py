#  This file is part of SALSA software
#
#  Copyright (c) 2022 - SALSA Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/biomics-pasteur-fr/salsa
#
##############################################################################
import click

from . import version
from .compute_ttest import compute_ttest

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version)
def main(**kwargs):
    """This is the main entry point for a set of applications provided
    by the SALSA group .

    """
    pass


main.add_command(compute_ttest)
