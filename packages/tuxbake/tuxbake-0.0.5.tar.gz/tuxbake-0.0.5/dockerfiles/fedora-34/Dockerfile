FROM fedora:34

ENV TOOLS_DIR=/home/tuxbitbake/tools
ENV PATH=${TOOLS_DIR}/bin:${PATH}
ENV LANG=en_US.UTF-8
# setting default shell to bash
ENV SHELL /bin/bash
ENV PKG_DEPS="\
    make \
    automake \
    gcc \
    gcc-c++ \
    kernel-devel \
    chrpath \
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
    openssh-server \
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
    glibc-devel \
    glibc-devel.i686 \
    lz4 \
    zstd \
    python2 \
    bzip2 \
    hostname \
    patch \
    rpcgen \
    which\
"

# Can be overriden at build time
ARG CI_RUNNER_PASSWORD=tuxbitbake


RUN set -e ;\
    dnf update --assumeyes;\
    dnf distro-sync --assumeyes ;\
    dnf install -y --nobest ${PKG_DEPS} ;\
    #Set Python 3 as default
    update-alternatives --install /usr/bin/python python /usr/bin/python2 73 ;\
    # Setup tuxbitbake user
    useradd -m -u 1001 -s /bin/bash tuxbitbake ;\
    echo "tuxbitbake:$CI_RUNNER_PASSWORD" | chpasswd ;\
    echo 'tuxbitbake ALL = NOPASSWD: ALL' > /etc/sudoers.d/ci ;\
    chmod 0440 /etc/sudoers.d/ci ;\
    # Run shell script(s) to install files, toolchains, etc...
    mkdir -p ${TOOLS_DIR}/bin ;\
    # Fix permissions
    chown -R tuxbitbake:tuxbitbake ${TOOLS_DIR} ;\
    # Cleanup
    #dnf clean ;\
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