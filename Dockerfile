########## How To Use Docker Image ###############
##
##  Image Name: 
##  Git link: 
##  How To Build Docker Image: docker build --no-cache -t denny/chatops_slack:v1 -f Dockerfile --rm=true .
##  Docker hub link:
##  Description:
##  Read more: https://www.dennyzhang.com/tag/chatops
##################################################
# Base Docker image: https://hub.docker.com/r/muccg/pylint/

FROM codacy/codacy-pylint:1.0.121

LABEL maintainer "Denny<https://www.dennyzhang.com/contact>"

USER root

RUN rm -rf /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip && \
    # Install packages required cryptography pip package
    apk add --update alpine-sdk && \
    apk add --update python-dev python3-dev py-pip gcc && \
    apk add --update libffi-dev && \
    apk add --update linux-headers && \
    apk add --update openssl-dev && \
    easy_install pip && \
    pip install uwsgi==2.0.15 && \
    # better way to deal with Flask installation
    (pip uninstall -y Flask || true) && pip install Flask==0.11.1 && \
    pip install paramiko==2.1.2 && \
    pip install slackclient==1.0.5 && \

# verify
   python --version && pip --version && \
   python --version | grep "3.5.1" && \
   pip --version | grep "9.0.1" && \
   pip show uwsgi | grep "2.0.15" && \
   pip show Flask | grep "0.11.1" && \
   pip show paramiko | grep "2.1.2" && \
   pip show slackclient | grep "1.0.5"

HEALTHCHECK --interval=5m --timeout=3s \
            CMD curl -f http://localhost:8081/chathelp || exit 1
