from multiprocessing import cpu_count

# Socket Path

bind = 'unix:/mnt/hard/PycharmProjects/OT/gunicorn.sock'



# Worker Options

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'



# Logging Options

loglevel = 'debug'

accesslog = '/mnt/hard/PycharmProjects/OT/access_log'

errorlog =  '/mnt/hard/PycharmProjects/OT/error_log'