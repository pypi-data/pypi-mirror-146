# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import requests
import os
import click
import zlib
import pathlib
from rich import print
from rich.progress import Progress


from hako.config import config
import base64
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from rich.prompt import Prompt

import tempfile


def _crc32(fileName):
    with open(fileName, "rb") as fh:
        file_hash = 0
        file_size = 0
        while True:
            s = fh.read(65536)
            file_size += len(s)
            if not s:
                break
            file_hash = zlib.crc32(s, file_hash)
        return "%08X" % (file_hash & 0xFFFFFFFF), file_size


def _upload_file(file_path, file_name: str, public: bool = False, encrypt: bool = False, salt: Optional[bytes] = None):

    # Compute the size and hash
    file_hash, file_size = _crc32(file_path)

    # Create the new file request
    new_file_request = {
        "filesystem_path": f"/{file_name}",
        "file_hash": file_hash,
        "file_size": file_size,
        "is_public": public,
        "is_encrypted": encrypt,
        "encryption_salt": base64.b64encode(salt).decode("utf-8") if salt else None,
    }

    # Upload the file
    request = requests.put(
        config.routes.upload_url, json=new_file_request, headers={"Authorization": f"Bearer {config.get_token()}"}
    )

    if request.status_code != 200:
        print(request.json())
        print(f"[red]Failed to upload file: {request.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    # Get the pre-signed url
    file_object = request.json()
    if file_object["presigned_upload_url"] is None:
        print(f"[red]Failed to upload file: {file_object.get('detail', 'Unspecified Error!')}[reset]")
        return

    # Actually upload the file
    path = pathlib.Path(file_path)
    total_size = path.stat().st_size

    with Progress(refresh_per_second=100) as progress:
        task1 = progress.add_task("[green]Uploading...", total=total_size)
        bytes_so_far = 0

        def _update_pbar(monitor):
            nonlocal bytes_so_far
            progress.update(task1, advance=monitor.bytes_read - bytes_so_far)
            bytes_so_far = monitor.bytes_read

        with open(file_path, "rb") as f:
            file_object["presigned_upload_url"]["fields"]["file"] = ("filename", f)
            e = MultipartEncoder(fields=file_object["presigned_upload_url"]["fields"])
            m = MultipartEncoderMonitor(e, _update_pbar)
            headers = {"Content-Type": m.content_type}
            r = requests.post(file_object["presigned_upload_url"]["url"], data=m, headers=headers)  # type: ignore

            # r = requests.post(
            #     file_object["presigned_upload_url"]["url"],
            #     data=file_object["presigned_upload_url"]["fields"],
            #     files={"file": open(file_path, "rb")},
            # )
            if r.status_code != 204:
                print(f"[red]Failed to upload file: {r.content}[reset]")
                return

    # Notify the server that the file has been uploaded
    request = requests.post(
        f"{config.routes.notify_uploaded_url}/{file_object['_id']}",
        headers={"Authorization": f"Bearer {config.get_token()}"},
    )

    if request.status_code != 200:
        print(f"[red]Failed to notify server: {request.json().get('detail', 'Unspecified Error!')}[reset]")
        return

    print("[green]File uploaded successfully![reset]")


@click.argument("file", type=click.Path(exists=True), required=True)
@click.option("--make_public", is_flag=True, default=False, help="Make the file public.")
@click.option("--encrypt", is_flag=True, default=False, help="Encrypt the file.")
def upload(file: str, make_public: bool = False, encrypt: bool = False) -> None:
    """Upload a file to Hako."""
    if not os.path.exists(file):
        print(f"[red]File does not exist: [white]{file}[reset]")
        return

    if not config.get_token():
        print("[red]You must be logged in to upload files! Login with `hako login`[reset]")
        return

    if encrypt:
        # Generate a salt
        salt = os.urandom(16)
        password = Prompt.ask("Enter a password to encrypt the file", password=True)
        confirm_password = Prompt.ask("Confirm the password", password=True)
        if password != confirm_password:
            print("[red]Passwords do not match!")
            return
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        print("[magenta]Generating key...[reset]")
        key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        f = Fernet(key)

        # Encrypt the file to a temporary file
        print("[magenta]Encrypting file...[reset]")
        with tempfile.NamedTemporaryFile() as tmp:
            with open(file, "rb") as fh:
                tmp.write(f.encrypt(fh.read()))
            tmp.flush()

            print("[magenta]Uploading file...[reset]")
            return _upload_file(tmp.name, os.path.basename(file), make_public, encrypt, salt)
    return _upload_file(file, os.path.basename(file), make_public, encrypt)
