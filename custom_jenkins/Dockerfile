# Use Jenkins base image
FROM jenkins/jenkins:lts

# Switch to root
USER root

# Install Python + Docker dependencies
RUN apt-get update -y && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    python3-venv

# Add Docker official GPG key
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
RUN echo \
    "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" \
    > /etc/apt/sources.list.d/docker.list

# Install Docker
RUN apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Create python alias
RUN ln -s /usr/bin/python3 /usr/bin/python

# Add Jenkins user to docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Docker storage
RUN mkdir -p /var/lib/docker

VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins