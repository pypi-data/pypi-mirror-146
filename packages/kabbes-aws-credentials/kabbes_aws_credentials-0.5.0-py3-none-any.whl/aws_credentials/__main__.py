import time
import aws_credentials

if aws_credentials.update():
    time.sleep( 1 )
else:
    time.sleep( 5 )

