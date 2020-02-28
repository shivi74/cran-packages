import os
from crontab import CronTab

cron = CronTab(user=os.environ['USER'])
job = cron.new(command='python package.py')
job.hour.on(12)
print(job)

cron.write()
