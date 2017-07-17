########## How To Use Docker Image ###############
##
##  Image Name: 
##  Git link: 
##  How To Build Docker Image: docker build --no-cache -t totvslabs/chatops:v1 -f Dockerfile_v1 --rm=true .
##  Docker hub link:
##  Description: 
##################################################
# Base image: https://raw.githubusercontent.com/DennyZhang/devops_docker_image/tag_v6/chatops/Dockerfile_v0

FROM denny/chatops:v0

LABEL maintainer "Denny<denny.zhang@totvs.com>"
