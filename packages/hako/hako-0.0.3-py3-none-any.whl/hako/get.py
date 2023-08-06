# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import requests
from .config import config
from rich.progress import track
import click
from rich import print

from rich.prompt import Prompt

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64

from io import BytesIO


def _get_file_unencrypted(file_data):
    # Get the file from S3
    s3_request = requests.get(
        file_data, allow_redirects=True, stream=True, headers={"Authorization": f"Bearer {config.get_token()}"}
    )
    if s3_request.status_code not in [200, 307]:
        print(f"[red]Failed to get files: {s3_request.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    file_name = s3_request.headers.get("Content-Disposition", "file").split("=")[1].replace('"', "")
    with open(file_name, "wb") as fh:
        total_size_in_bytes = int(s3_request.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        for data in track(
            s3_request.iter_content(block_size),
            description=f"Downloading {file_name}",
            total=total_size_in_bytes // block_size + 1,
        ):
            fh.write(data)
    print("[green]Finished downloading![reset]")


def _get_file_encrypted(file_data, salt):

    # Download the URL into bytes
    s3_request = requests.get(file_data, allow_redirects=True, stream=True)
    file_name = s3_request.headers.get("Content-Disposition", "file").split("=")[1].replace('"', "")
    bytes_io = BytesIO()
    for data in track(
        s3_request.iter_content(1024),
        description=f"Downloading {file_name}",
        total=int(s3_request.headers.get("content-length", 0)) // 1024 + 1,
    ):
        bytes_io.write(data)

    # Decrypt the file
    password = Prompt.ask("Enter password to decrypt the file", password=True)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base64.b64decode(salt.encode("utf-8")),
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    f = Fernet(key)

    # Decrypt the file
    bytes_io.seek(0)
    try:
        decrypted_data = f.decrypt(bytes_io.read())
    except InvalidToken:
        print("[red]Unable to decrypt file: Invalid password![reset]")
        return

    # Write the decrypted data to a file
    with open(file_name, "wb") as fh:
        fh.write(decrypted_data)
    print("[green]Finished downloading![reset]")


@click.argument("filename", type=str)
def get(filename: str):
    """List all files in the given prefix"""
    files = requests.get(config.routes.list_files_url, headers={"Authorization": f"Bearer {config.get_token()}"})
    if files.status_code != 200:
        print(f"[red]Failed to get files: {files.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    file_to_get = None
    for file in files.json():
        for owner in file["owners"]:
            if file["filesystem_paths"][owner][1:] == filename:
                file_to_get = file
                break
    if file_to_get is None:
        print(f"[red]Failed to get {filename}: File not found![reset]")
        return

    # Download the file
    # file_url =
    # request = requests.get(file_url, headers={"Authorization": f"Bearer {config.get_token()}"})
    # if request.status_code != 200:
    #     print(f"[red]Failed to download file: {request.json().get('detail', 'Unspecified Error!')}[reset]")
    #     return
    # file_data = request.json()

    if not file_to_get["is_encrypted"]:
        _get_file_unencrypted(config.routes.download_file_url_fmtstring.format(file_to_get["_id"]))
    else:
        _get_file_encrypted(
            config.routes.download_file_url_fmtstring.format(file_to_get["_id"]), salt=file_to_get["encryption_salt"]
        )
