import shutil
import os

TOPDIR = os.path.dirname(os.path.abspath(__file__))

class Updater(object):

    def __init__(self, name, download_path, install_path):
        self.name = name
        self.download_path = download_path
        self.install_path = install_path

    def install(self):
        src = os.path.join(self.download_path, self.name)
        dst = os.path.join(self.install_path, self.name)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)

        helpers = os.path.join(TOPDIR, 'helpers/{}'.format(self.name))
        if os.path.exists(helpers):
            shutil.copytree(helpers, dst, dirs_exist_ok=True)
