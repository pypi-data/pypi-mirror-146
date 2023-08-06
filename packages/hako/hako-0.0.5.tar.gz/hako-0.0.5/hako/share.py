# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import click
import requests
import pick
import datetime

from rich import print

from .config import config


@click.argument(
    "filename",
    type=str,
    required=False,
)
def share(filename: str):
    """Generate a link for file sharing

    Args:
        filename (str): The file to share
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
        file_to_share = file_list[index][1]
    else:
        # Get the file from the file name
        files = requests.get(config.routes.list_files_url, headers={"Authorization": f"Bearer {config.get_token()}"})
        if files.status_code != 200:
            print(f"[red]Failed to get files: {files.json().get('detail', 'Unspecified Error!')}[reset]")
            return

        file_to_share = None
        for file in files.json():
            for owner in file["owners"]:
                if file["filesystem_paths"][owner][1:] == filename:
                    file_to_share = file
                    break

    if file_to_share is None:
        print(f"[red]Failed to find file: {filename}[reset]")
        return

    # Prompt user for share expiration
    expiration_hours = click.prompt("Enter the number of hours the share should be valid for", type=int, default=24)

    # Share the file
    r = requests.put(
        config.routes.share_create_fmt_string.format(file_to_share["_id"], expiration_hours),
        headers={"Authorization": f"Bearer {config.get_token()}"},
    )

    if r.status_code != 200:
        print(f"[red]Failed to share file: {r.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    data = r.json()
    url = config.routes.base + data["url"]

    print(
        f"[green]Successfully shared file: {file_to_share['filesystem_paths'][file_to_share['owners'][0]][1:]}[reset]"
    )
    print(f"[green]Download link: [u]{url}[reset]")
    print(f"[green]Get this file with: `curl -JLO {url}`[reset]")
    print(f"[green]Share expires in {expiration_hours} hours[reset]")


@click.argument(
    "filename",
    type=str,
    required=False,
)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Delete all shares for the file",
)
def unshare(filename: str, all: bool = False):
    """Remove a link to a shared file (Does not remove the file)

    Args:
        filename (str): The file to unshare
        all (bool, optional): If all links should be removed. Defaults to False.
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
        _, index = pick.pick([f[0] for f in file_list], "Select a file to unshare")
        file_to_unshare = file_list[index][1]
    else:
        # Get the file from the file name
        files = requests.get(config.routes.list_files_url, headers={"Authorization": f"Bearer {config.get_token()}"})
        if files.status_code != 200:
            print(f"[red]Failed to get files: {files.json().get('detail', 'Unspecified Error!')}[reset]")
            return

        file_to_unshare = None
        for file in files.json():
            for owner in file["owners"]:
                if file["filesystem_paths"][owner][1:] == filename:
                    file_to_unshare = file
                    break

    if file_to_unshare is None:
        print(f"[red]Failed to find file: {filename}[reset]")
        return

    if len(file_to_unshare["shares"]) == 0:
        print(f"[red]No shares to delete for file: {filename}[reset]")
        return

    # Get a list of all shares for the file
    all_shares = []
    for share_id in file_to_unshare["shares"]:
        r = requests.get(
            config.routes.share_fmt_string.format(share_id), headers={"Authorization": f"Bearer {config.get_token()}"}
        )
        if r.status_code != 200:
            print(f"[red]Failed to get share: {r.json().get('detail', 'Unspecified Error!')}[reset]")
            return

        if r.json()["expired"]:
            continue
        all_shares.append(r.json())

    shares_to_delete = []
    if all:
        shares_to_delete = all_shares
    else:
        # Prompt the user for a share to delete
        exp_string = [
            (
                f"Expires in {round((datetime.datetime.fromisoformat(s['expiration']) - datetime.datetime.now()).total_seconds() / 3600, 1)} hours"
                if s["expiration"] is not None
                else "Does not expire"
            )
            for s in all_shares
        ]
        url_string = [f'{config.routes.base}{s["url"]} ({e})' for s, e in zip(all_shares, exp_string)]

        if not url_string:
            print("[red]No shares found to delete![reset]")
            return
        elif len(url_string) == 1:
            index = 0
        else:
            _, index = pick.pick(url_string, "Select a share to delete")
        shares_to_delete.append(all_shares[index])

    for s in shares_to_delete:
        r = requests.delete(
            config.routes.share_delete_fmt_string.format(s["share_id"]),
            headers={"Authorization": f"Bearer {config.get_token()}"},
        )
        if r.status_code != 200:
            print(f"[red]Failed to delete share: {r.json().get('detail', 'Unspecified Error!')}[reset]")
            continue
        print(f"[green]Successfully deleted share: {config.routes.base + s['url']}[reset]")
