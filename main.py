from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import zmail
from pynvml import *

"""
pip install apscheduler
pip install nvidia-ml-py3
pip install zmail
"""

#=========== Server configuration ===========
SERVER = 'xxxx@163.com'
CODE = 'xxxxx'
PWD = 'xxxx'
server = zmail.server(SERVER, CODE)
#=========== Server configuration finish ===========================


#============ config your email address=========
client_email = 'your email address'
# your email content
mail_content = {
    'subject': 'Success!',  # subject
    'content_text': 'gpu is free!',
}

gpu_id = 0   # monitor GPU:0
free_thresh = 20  # if GPU:0 has at least 20GB memory, then send an email
interval_minutes = 2  # check once gpu usage every 2 minutes
#================================================


def get_gpu_usage_by_id(gpu_id:int, free_thresh:int):
    """
    gpu_id: int, the id of gpu need monitoring. For example, we want to monitor GPU:0, then set gpu_id=0 is ok
    free_thresh: int, free memory. For example, we expect GPU:0 to have at least 20GB free memory, just set free_thresh=20
    """
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(gpu_id)
    info = nvmlDeviceGetMemoryInfo(handle)
    free = info.free/1e9
    nvmlShutdown()
    return free > free_thresh, free
        
def monitor_gpu_usage(gpu_id, free_thresh):
    flag, free = get_gpu_usage_by_id(gpu_id, free_thresh)
    if flag:
        success = server.send_mail(client_email, mail_content)
        if success:
            sched.shutdown(wait=False)    

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(monitor_gpu_usage, 'interval',  minutes=interval_minutes, kwargs={'gpu_id': gpu_id, 'free_thresh': free_thresh})
    sched.start()
