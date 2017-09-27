#!/bin/bash -e
cd /code

echo "remove pyc files"
find . -type f -name "*.pyc" -print0 | xargs rm -rf

# TODO: verify config.py is configured

# TODO: show warning, if ssh key file is not there

uwsgi -w wsgi --http-socket :8081 --enable-threads --vacuum --logto /tmp/uwsgi-wsgi.log
# tail -f /tmp/uwsgi-wsgi.log

## File : docker-entrypoint.sh ends
