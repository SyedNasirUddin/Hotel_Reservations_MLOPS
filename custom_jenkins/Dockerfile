FROM jenkins/jenkins:lts

USER root

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg

# Make python command available
RUN ln -sf /usr/bin/python3 /usr/bin/python



# Add Jenkins user permissions
RUN groupadd -f docker && \
    usermod -aG docker jenkins && \
    usermod -aG root jenkins

USER jenkins