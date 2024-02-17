# # bash parameter expansion: assign a DEFAULT value when environment variable not set or null

# PORT will be set to '5000' if APP_PORT not set or null. The value of APP_PORT remains not set.
# PORT="${APP_PORT:-5000}"

# if APP_PORT not set or null, set it's value to '5000'. Then that value will be set to PORT.
PORT="${APP_PORT:=5000}"
THREADS="${APP_THREADS:=1}"
WORKERS="${APP_WORKERS:=1}"
TIMEOUT="${APP_TIMEOUT:=30}"

#--worker-class gevent

exec gunicorn --workers=$WORKERS --threads=$THREADS --timeout $TIMEOUT -b 0.0.0.0:$PORT --chdir . wsgi:app
