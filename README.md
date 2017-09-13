[![Build Status](https://travis-ci.org/DennyZhang/chatops_slack.svg?branch=master)](https://travis-ci.org/DennyZhang/chatops_slack) [![LinkedIn](https://www.dennyzhang.com/wp-content/uploads/sns/linkedin.png)](https://www.linkedin.com/in/dennyzhang001) [![Github](https://www.dennyzhang.com/wp-content/uploads/sns/github.png)](https://github.com/DennyZhang) [![Twitter](https://www.dennyzhang.com/wp-content/uploads/sns/twitter.png)](https://twitter.com/dennyzhang001) [![Slack](https://www.dennyzhang.com/wp-content/uploads/sns/slack.png)](https://www.dennyzhang.com/slack)
- File me [tickets](https://github.com/DennyZhang/chatops_slack/issues) or star [this github repo](https://github.com/DennyZhang/chatops_slack)

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
```
Check: docker-entrypoint.sh

tail -f /tmp/uwsgi-wsgi.log

docker-compose down && docker-compose up -d && docker exec -it devops_chatops tail -f /tmp/uwsgi-wsgi.log
```

Discuss with Denny in [LinkedIn](https://www.linkedin.com/in/dennyzhang001) or [Blog](https://www.dennyzhang.com).
