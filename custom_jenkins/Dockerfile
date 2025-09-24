## Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

## Switch to root user to install dependencies
USER root

## Install prerequisites and Docker using Docker’s convenience script
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg lsb-release && \
    curl -fsSL https://get.docker.com | sh && \
    apt-get clean

## Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

## Create the Docker directory and volume for DinD (Docker in Docker)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

## Switch back to the Jenkins user
USER jenkins