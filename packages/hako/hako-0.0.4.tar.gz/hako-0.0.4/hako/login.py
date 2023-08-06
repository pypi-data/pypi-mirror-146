# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from rich.prompt import Prompt
from rich import print

import base64
import requests

from .config import config


def login():
    """Login to Hako."""
    username = Prompt.ask("Enter your username")
    password = Prompt.ask("Enter your password", password=True)

    # Make a HTTPS request to the server for a token
    try:
        response = requests.post(
            config.routes.token_url,
            data={
                "username": username,
                "password": password,
            },
        )
        rsp = response.json()
        if response.status_code == 200:
            token = rsp["access_token"]
            # Save the token to the local auth file
            config.token = token
            config.save()
            print(f"[green]Successfully logged in as {username}![reset]")
        else:
            print(f"[red]Failed to login: {rsp['message']}[reset]")
    except Exception as ex:
        print(f"[red]Failed to login: {ex}[reset]")
