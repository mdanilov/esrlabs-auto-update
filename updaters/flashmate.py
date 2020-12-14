import updater
import urllib.parse
import requests
import os
import shutil
import json

from utils import *
from updater import *


class Flashmate(Updater):
    ARTIFACTORY_URL = 'https://artifactory.int.esrlabs.com/artifactory/'

    def __init__(self, download_path, install_path):
        super().__init__('flashmate', download_path, install_path)

    def check_updates(self):
        tool_path = os.path.join(self.install_path, self.name)
        jar_file = os.path.join(tool_path, 'flashmate.jar')
        if not os.path.exists(jar_file):
            return True

        old_sha1 = get_sha1_digest(jar_file)
        url = urllib.parse.urljoin(
            self.ARTIFACTORY_URL, 'api/storage/esr-flashmate-local/latest/flashmate.jar')
        r = requests.get(url)
        sha1 = json.loads(r.content)['checksums']['sha1']
        return old_sha1 != sha1

    def download(self):
        dst = os.path.join(self.download_path, self.name)
        shutil.rmtree(dst, ignore_errors=True)
        os.makedirs(dst, exist_ok=True)
        files = ['flashmate.jar', 'ChangeLog.md']
        for file in files:
            url = urllib.parse.urljoin(
                self.ARTIFACTORY_URL, 'esr-flashmate-local/latest/{}'.format(file))
            r = requests.get(url)
            if r.ok:
                open(os.path.join(dst, file),
                     'wb').write(r.content)
                return True

    def install(self):
        return super().install()
