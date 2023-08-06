import sys
sys_args = sys.argv[1:]

from aws_credentials import update

SUCCESS_SLEEPY_TIME = 1
ERROR_SLEEPY_TIME = 5

if update():
    time.sleep( SUCCESS_SLEEPY_TIME )
else:
    time.sleep( ERROR_SLEEPY_TIME )

