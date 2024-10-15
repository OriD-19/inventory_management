import os

workers = 1
bind = "127.0.0.1:"+os.environ.get("PORT", "8080")
log_level = 'info'
accesslog = '-'
capture_output = True
timeout = 180

#worker_class = 'gevent'