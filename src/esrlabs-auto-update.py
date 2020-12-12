import click
import requests
import hashlib
import urllib.parse
import shutil
import json
import os

TOOLS_DIR = 'esrlabs-tools'
ARTIFACTORY_URL = 'https://artifactory.int.esrlabs.com/artifactory/'
SCRIPT_DIR = os.path.dirname(__file__)


def get_sha1_digest(file):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def check_updates():
    tool_path = os.path.join(install_dir, 'flashmate')
    old_sha1 = get_sha1_digest(os.path.join(tool_path, 'flashmate.jar'))
    url = urllib.parse.urljoin(ARTIFACTORY_URL, 'api', 'storage', 'esr-flashmate-local',
                        'latest', 'flashmate.jar')
    r = requests.get(url)
    sha1 = json.loads(r.content)['checksums']['sha1']
    return old_sha1 != sha1


def install(install_dir):
    tool_path = os.path.join(install_dir, 'flashmate')
    os.makedirs(tool_path, exist_ok=True)
    files = ['flashmate.jar', 'ChangeLog.md']
    for file in files:
        url = urllib.parse.urljoin(ARTIFACTORY_URL, f'esr-flashmate-local/latest/{file}')
        r = requests.get(url)
        if r.ok:
            open(os.path.join(tool_path, file),
                'wb').write(r.content)
    shutil.copy(os.path.join(
        SCRIPT_DIR, '../helpers/flashmate/flashmate'), tool_path)
    shutil.copy(os.path.join(
        SCRIPT_DIR, '../helpers/flashmate/flashmate.bat'), tool_path)


@click.command()
@click.option(
    '--install-dir',
    type=click.Path(exists=True),
    help='File path in which all esrlabs tools will be installed.'
    'If not provided, a prompt will allow you to type the input text.'
)
def main(install_dir):
    if not install_dir:
        install_dir = click.prompt('Enter a install dir', type=click.Path(
            exists=True))

    install(os.path.join(install_dir, TOOLS_DIR))


if __name__ == '__main__':
    main()
