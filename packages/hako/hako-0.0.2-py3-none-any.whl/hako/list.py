# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import requests
from .config import config
from rich import print
from rich.rule import Rule

import datetime


def ls():
    """List all files in the given prefix"""
    files = requests.get(config.routes.list_files_url, headers={"Authorization": f"Bearer {config.get_token()}"})
    if files.status_code != 200:
        print(f"[red]Failed to list files: {files.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    print(Rule(title=f"{len(files.json())} file{'s' if len(files.json()) > 1 else ''} found"))
    for file in files.json():
        file_url = config.routes.download_file_url_fmtstring.format(file["_id"])
        estring = ", Encrypted" if file["is_encrypted"] else ""
        file_url_string = (
            f"[magenta][u]{file_url}{estring}[reset]"
            if file["is_public"]
            else "[magenta](Not Public, Not Shared)[reset]"
        )

        file_share_url_string = f"[u]{file_url}[/u]" if file["is_public"] else ""
        share_output_strings = []
        for share in file["shares"]:
            # Get the file share URL
            r = requests.get(
                config.routes.share_fmt_string.format(share), headers={"Authorization": f"Bearer {config.get_token()}"}
            )
            if r.status_code != 200:
                print(f"[red]Failed to get share URL: {r.json().get('detail', 'Unspecified Error!')}[reset]")
                continue
            data = r.json()
            if data["expired"]:
                continue
            exp_string = (
                f"Expires in {round((datetime.datetime.fromisoformat(data['expiration']) - datetime.datetime.now()).total_seconds() / 3600, 1)} hours"
                if data["expiration"] is not None
                else "Does not expire"
            )
            url_string = f'[u]{config.routes.base}{data["url"]}[/u]'
            share_output_strings.append(f"  Shared at: [green]{url_string} ({exp_string})[reset]")

        file_attribute_string = f"{file['file_size']} bytes{', Not Public' if not file['is_public'] else ''}{', Encrypted' if file['is_encrypted'] else ''}{', Shared' if len(share_output_strings) > 0 else ''}"

        file_url_string = f"[magenta]({file_attribute_string})[reset]"
        file_name_string = f"[green]{file['filesystem_paths'][file['owners'][0]][1:]}[reset]"
        print(f"{file_name_string}\t{file_url_string}")
        if file["is_public"]:
            print(f"  Is public at: [green]{file_share_url_string}[reset]")
        for share_output_string in share_output_strings:
            print(share_output_string)
