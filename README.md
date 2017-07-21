- Check more: https://www.dennyzhang.com/chatqueryhost
- Reference: https://github.com/slackapi/Slack-Python-Onboarding-Tutorial

# Limitation
- Only Python3 is supported. (Use docker image by default)

# Setup the env via docker

1. Prepare ssh_id_rsa and config.py

2. docker-compose up -d

# Setup in client nodes
```
wget -O /usr/sbin/node_usage.py \
     https://raw.githubusercontent.com/DennyZhang/devops_public/tag_v6/python/node_usage/node_usage.py
```

# Useful commands

Check: docker-entrypoint.sh

tail -f /tmp/uwsgi-wsgi.log

docker-compose down && docker-compose up -d && docker exec -it devops_chatops tail -f /tmp/uwsgi-wsgi.log
