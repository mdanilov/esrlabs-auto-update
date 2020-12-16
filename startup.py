import getpass
import platform
import os

from crontab import CronTab


def set_startup_rules(filename):
    if platform.system() == 'Linux':
        command = 'nohup python3 {} &'.format(os.path.abspath(filename))
        username = getpass.getuser()
        cron = CronTab(user=username)
        for job in cron:
            if job.comment == 'esrlabs-auto-update':
                cron.remove(job)
                break
        job = cron.new(command=command, comment='esrlabs-auto-update')
        job.every_reboot()
        cron.write()
