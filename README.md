Python slack ChatOps

<a href="https://github.com/DennyZhang?tab=followers"><img align="right" width="200" height="183" src="https://www.dennyzhang.com/wp-content/uploads/denny/watermark/github.png" /></a>

[![Build Status](https://travis-ci.org/DennyZhang/chatops_slack.svg?branch=master)](https://travis-ci.org/DennyZhang/chatops_slack) [![Docker](https://www.dennyzhang.com/wp-content/uploads/sns/docker.png)](https://hub.docker.com/r/denny/chatops_slack/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[![LinkedIn](https://www.dennyzhang.com/wp-content/uploads/sns/linkedin.png)](https://www.linkedin.com/in/dennyzhang001) [![Github](https://www.dennyzhang.com/wp-content/uploads/sns/github.png)](https://github.com/DennyZhang) [![Twitter](https://www.dennyzhang.com/wp-content/uploads/sns/twitter.png)](https://twitter.com/dennyzhang001) [![Slack](https://www.dennyzhang.com/wp-content/uploads/sns/slack.png)](https://goo.gl/ozDDyL)

- File me [tickets](https://github.com/DennyZhang/chatops_slack/issues) or star [the repo](https://github.com/DennyZhang/chatops_slack)

- Check more: https://www.dennyzhang.com/tag/chatops

# System Design
- Limitation: Only Python3 is supported. (Use [docker](./docker-compose.yml) to deploy by default).

# Major Default Slack Bots
```
DevOps ChatOps via Slack Commands. All commands starts with /chat*
- /chatclusterusage: Overall resource usage, and summary by role.
- /chatcloudexpense: Show cloud bills across different cloud providers.
- /chatqueryhost [substring of hostname]: Query host without manual ssh.
- /chathelp: Current online help usage
```
- TODO: guide people to add their own, if they want

# How To Use
## 1. Setup ChatOps Server via docker-compose

1.1. Prepare ssh_id_rsa and config.py

1.2. docker-compose up -d

## 2. Setup in client nodes
```
wget -O /usr/sbin/node_usage.py \
     https://raw.githubusercontent.com/DennyZhang/devops_public/tag_v6/python/node_usage/node_usage.py
```

## 3. Create slack commands in Slack setting page
Configure Slack Commands for each python flask endpoint.

## 4. Try the bots in Slack
![](https://raw.githubusercontent.com/DennyZhang/chatops_slack/master/images/chatops.jpg)

# Useful commands
```
Check: docker-entrypoint.sh

tail -f /tmp/uwsgi-wsgi.log

docker-compose down && docker-compose up -d \
  && docker exec -it devops_chatops tail -f /tmp/uwsgi-wsgi.log
```

# Limitation
1. Query nodes from slack, we use ssh private key. Here we assume one private key can login to all related nodes

# More Resources
- Reference: https://github.com/slackapi/Slack-Python-Onboarding-Tutorial
