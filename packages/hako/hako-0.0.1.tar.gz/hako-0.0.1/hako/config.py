# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Union
import requests

from rich import print


@dataclass
class Routes:
    token_url: str = "https://hako.isx.ai/api/v0/token"
    upload_url: str = "https://hako.isx.ai/api/v0/files/new_file"
    notify_uploaded_url: str = "https://hako.isx.ai/api/v0/files/notify_uploaded"
    list_files_url: str = "https://hako.isx.ai/api/v0/files/list"
    download_file_url_fmtstring: str = "https://hako.isx.ai/api/v0/f/{}"
    delete_file_url_fmtstring: str = "https://hako.isx.ai/files/{}?force=true"
    share_fmt_string: str = "https://hako.isx.ai/share/info/{}"
    share_delete_fmt_string: str = "https://hako.isx.ai/files/share/{}"
    share_create_fmt_string: str = "https://hako.isx.ai/files/share/{}?expiration={}"
    token_validate_url: str = "https://hako.isx.ai/api/v0/token/validate"
    base: str = "https://hako.isx.ai"


@dataclass
class DebugRoutes:
    token_url: str = "http://localhost:8000/token"
    upload_url: str = "http://localhost:8000/files/new_file"
    notify_uploaded_url: str = "http://localhost:8000/files/notify_uploaded"
    list_files_url: str = "http://localhost:8000/files/list"
    download_file_url_fmtstring: str = "http://localhost:8000/f/{}"
    delete_file_url_fmtstring: str = "http://localhost:8000/files/{}?force=true"
    share_fmt_string: str = "http://localhost:8000/share/info/{}"
    share_delete_fmt_string: str = "http://localhost:8000/files/share/{}"
    share_create_fmt_string: str = "http://localhost:8000/files/share/{}?expiration={}"
    token_validate_url: str = "http://localhost:8000/token/validate"
    base: str = "http://localhost:8000"


@dataclass
class Config:
    """
    Configuration for the Hako client.
    """

    token: str = ""
    encryption_key: str = ""
    routes: Union[Routes, DebugRoutes] = Routes()

    def get_token(self):
        """
        Gets the token from the configuration file.
        """
        if not self.token:
            print("[red]No authentication token found. Please run `hako login` to login to Hako.[reset]")
            exit(1)
        # Validate the token
        r = requests.post(f"{self.routes.token_validate_url}", headers={"Authorization": f"Bearer {self.token}"})
        if r.status_code != 200:
            print("[red]Invalid authentication token. Please run `hako login` to login to Hako.[reset]")
            self.token = ""
            self.save()
            exit(1)

        return self.token

    @classmethod
    def from_env(cls):
        """
        Loads the configuration from environment variables.
        """
        return cls(
            token=os.environ.get("HAKO_TOKEN", ""),
            encryption_key=os.environ.get("HAKO_ENCRYPTION_KEY", ""),
        )

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        """
        Loads the configuration from a file.
        """
        return cls(**json.loads(path.read_text()))

    def env_override(self):
        """
        Overrides the configuration with environment variables.
        """
        return Config(
            token=os.environ.get("HAKO_TOKEN", self.token),
            encryption_key=os.environ.get("HAKO_ENCRYPTION_KEY", self.encryption_key),
        )

    def save(self):
        """
        Saves the configuration to a file.
        """
        (Path.home() / ".hakorc").write_text(
            json.dumps(
                {
                    "token": self.token,
                    "encryption_key": self.encryption_key,
                }
            )
        )


rcpath = Path.home() / ".hakorc"
if rcpath.exists():
    config = Config.from_file(rcpath)
    config = config.env_override()
else:
    config = Config.from_env()
