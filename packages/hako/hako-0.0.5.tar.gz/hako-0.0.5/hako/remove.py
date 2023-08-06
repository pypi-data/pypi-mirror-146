# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import click
from .config import config
import requests
import pick

from rich.prompt import Confirm
from rich import print


@click.argument(
    "filename",
    type=str,
    required=False,
)
def rm(filename: str):
    """Remove a file from Hako

    Args:
        filename (str): The file to remove
    """

    if filename is None:
        # Get a list of all files
        all_files = requests.get(
            config.routes.list_files_url, headers={"Authorization": f"Bearer {config.get_token()}"}
        )
        if all_files.status_code != 200:
            print(f"[red]Failed to list files: {all_files.json().get('detail', 'Unspecified Error!')}[reset]")
            return

        file_list = [(file["filesystem_paths"][file["owners"][0]][1:], file) for file in all_files.json()]

        # Prompt the user for a file to delete
        _, index = pick.pick([f[0] for f in file_list], "Select a file to delete")
        file_to_rm = file_list[index][1]
    else:
        # Get the file from the file name
        files = requests.get(config.routes.list_files_url, headers={"Authorization": f"Bearer {config.get_token()}"})
        if files.status_code != 200:
            print(f"[red]Failed to get files: {files.json().get('detail', 'Unspecified Error!')}[reset]")
            return

        file_to_rm = None
        for file in files.json():
            for owner in file["owners"]:
                if file["filesystem_paths"][owner][1:] == filename:
                    file_to_rm = file
                    break

    if file_to_rm is None:
        print(f"[red]Failed to find file: {filename}[reset]")
        return

    # Prompt the user to confirm the deletion
    if not Confirm.ask(
        f"Are you sure you want to delete {file_to_rm['filesystem_paths'][file_to_rm['owners'][0]][1:]}?"
    ):
        print("[red]Cancelled deletion[reset]")
        return

    # Delete the file
    response = requests.delete(
        config.routes.delete_file_url_fmtstring.format(file_to_rm["_id"]),
        headers={"Authorization": f"Bearer {config.get_token()}"},
    )
    if response.status_code != 200:
        print(f"[red]Failed to delete file: {response.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    print(f"[green]Successfully deleted file: {file_to_rm['filesystem_paths'][file_to_rm['owners'][0]][1:]}[reset]")
