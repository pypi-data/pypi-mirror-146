FROM opensuse/leap:15.2

ENV TOOLS_DIR=/home/tuxbitbake/tools
ENV PATH=${TOOLS_DIR}/bin:${PATH}
ENV LANG=en_US.UTF-8
ENV PKG_DEPS="\
    gcc \
    gcc-c++ \
    make \
    chrpath \
    python-xml \
    python-curses \
    python3-curses \
    cpio \
    curl \
    diffstat \
    file \
    gawk \
    git \
    gnupg \
    iputils \
    jq \
    less \
    openssh \
    pigz \
    python3 \
    python3-pip \
    socat \
    sudo \
    texinfo \
    unzip \
    wget \
    xz \
    xmlstarlet \
    awscli \
    openssl-devel \
    #libc6-dev-i386 \
    lz4 \
    zstd \
    python2 \
    patch \
    bzip2 \
    gzip \
    hostname \
    tar \
    which \
"

# Can be overriden at build time
ARG CI_RUNNER_PASSWORD=tuxbitbake


RUN set -e ;\
    zypper -nq update ;\
    zypper -nq dist-upgrade ;\
    zypper -nq install --no-recommends ${PKG_DEPS} ;\
    # Set default shell to bash
    chsh -s /usr/bin/sh ;\
    # Set Python 3 as default
    update-alternatives --install /usr/bin/python python /usr/bin/python2 73 ;\
    # Setup tuxbitbake user
    useradd -m -U -u 1001 -s /bin/bash tuxbitbake ;\
    echo "tuxbitbake:$CI_RUNNER_PASSWORD" | chpasswd ;\
    echo 'tuxbitbake ALL = NOPASSWD: ALL' > /etc/sudoers.d/ci ;\
    chmod 0440 /etc/sudoers.d/ci ;\
    # Run shell script(s) to install files, toolchains, etc...
    mkdir -p ${TOOLS_DIR}/bin ;\
    # Fix permissions
    chown -R tuxbitbake:tuxbitbake ${TOOLS_DIR} ;\
    # Cleanup
    zypper clean ;\
    rm -rf /var/lib/apt/lists/* /tmp/*

USER tuxbitbake

RUN set -e ;\
    # Set git default config
    git config --global user.email "ci@tuxsuite.com" ;\
    git config --global user.name "Tuxsuite Bot" ;\
    git config --global color.ui "auto" ;\
    echo "progress = dot" > ${HOME}/.wgetrc ;\
    echo "dot_bytes = 10m" >> ${HOME}/.wgetrc

WORKDIR /home/tuxbitbake
CMD ["/bin/bash"]
