# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import click

from .upload import upload
from .list import ls
from .login import login
from .get import get
from .remove import rm
from .share import share, unshare


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


main.command(ls)
main.command(upload)
main.command(login)
main.command(get)
main.command(rm)
main.command(share)
main.command(unshare)
