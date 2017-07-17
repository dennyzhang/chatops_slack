#!/bin/bash -e
cd /code
echo "remove pyc files"
find . -name "*.pyc" | xargs rm -rf

uwsgi -w wsgi --http-socket :8081 --enable-threads --vacuum --logto /tmp/uwsgi-wsgi.log
# tail -f /tmp/uwsgi-wsgi.log
## File : docker-entrypoint.sh ends
