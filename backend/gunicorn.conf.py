bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "debug"
accesslog = None
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
proc_name = "Application Name"