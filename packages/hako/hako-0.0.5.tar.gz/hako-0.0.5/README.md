<!--
 Copyright (c) 2022 David Chan

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Hako: Command Line Cloud Storage

Hako is a command line cloud storage client, intefacing with the Hako server backend.

## Installation

To install the Hako client, use `pip install hako`

## Usage

Using the client requires logging in. To login, use `hako login`. This will prompt you for a username and password, and will
store an authentication token at `~/.hakorc`.

To list the files available in your cloud storage, run `hako ls`.

To upload a file, use `hako upload <filename>`. Currently, filenames in the server must be unique. Two options can be added: `--encrypt` and `--make_public`. Public files are accessible to any user through the generated link, while encrypted files will require this CLI to download (along with a password entered by the user). Files are encrypted end to end with SHA256 encryption.

To share a file, use `hako share <filename>`. This will generate a link that can be used to share the file over a standard web browser, or using wget from the command line. To delete this link (and prevent further downloads), use `hako unshare <filename>`.

To remove a file, use `hako rm <filename>`.
