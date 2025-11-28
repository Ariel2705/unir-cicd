FROM jenkins/jenkins:lts

USER root

# instalar make y docker cli
RUN apt-get update && \
    apt-get install -y make docker.io && \
    apt-get clean

# agregar jenkins al grupo docker
RUN usermod -aG docker jenkins

USER jenkins


# docker run -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock  jenkins-make
