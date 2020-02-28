# Creates a cronjob using python cronjob to run everyday 12 AM

import os
from crontab import CronTab

cron = CronTab(user=os.environ.get('USER'))
job = cron.new(command='python package.py')
job.hour.on(12)
print(job)

cron.write()
