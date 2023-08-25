from multiprocessing import cpu_count



# Socket Path

#bind = 'unix:/home/developer/backend/gunicorn.sock'
bind = '0.0.0.0:8000'


# Worker Options

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'



# Logging Options

loglevel = 'debug'

accesslog = '/home/developer/backend/access_log'

errorlog =  '/home/developer/backend/error_log'# test
