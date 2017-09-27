#!/bin/bash -e
cd /code

# Precheck
if [ ! -f config.py ]; then
    echo "ERROR: config.py is not found. See sample in config.py.template"
    exit 1
fi

if [ ! -f ssh_id_rsa ]; then
    echo "Warning: ssh_id_rsa is not found. Some slack commands may not work."
fi

################################################################################
echo "remove pyc files"
find . -type f -name "*.pyc" -print0 | xargs rm -rf

# Start the service
uwsgi -w wsgi --http-socket :8081 --enable-threads --vacuum --logto /tmp/uwsgi-wsgi.log
# tail -f /tmp/uwsgi-wsgi.log
## File : docker-entrypoint.sh ends
