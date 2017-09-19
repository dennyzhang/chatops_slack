########## How To Use Docker Image ###############
##
##  Image Name: 
##  Git link: 
##  How To Build Docker Image: docker build --no-cache -t denny/chatops_slack:v1 -f Dockerfile_v1 --rm=true .
##  Docker hub link:
##  Description: 
##################################################
# Base image: https://github.com/DennyZhang/chatops_slack/blob/master/Dockerfile

FROM denny/chatops:v0

LABEL maintainer "Denny<denny.zhang@totvs.com>"
