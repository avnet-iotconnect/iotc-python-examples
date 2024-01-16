FROM crops/poky:ubuntu-22.04

# Update package lists and install rsync
USER root
RUN apt-get update && \
    apt-get install -y \
    bsdmainutils \
    libgmp-dev \
    libmpc-dev \
    libssl-dev \
    python3-pip

# Switch back to the original user
USER usersetup

