FROM centos:centos8

ENV TOOLS_DIR=/home/tuxbitbake/tools
ENV PATH=${TOOLS_DIR}/bin:${PATH}
ENV LANG=en_US.UTF-8
ENV PKG_DEPS="\
    epel-release \
    gcc \
    gcc-c++ \
    make \ 
    chrpath \
    cpio \
    curl \
    diffstat \
    file \
    gawk \
    git \
    gnupg \
    iputils\
    jq -y \
    less \
    openssh \
    pigz \
    python3 \
    python3-pip \
    socat \
    sudo \
    unzip \
    wget \
    xz \
    #xmlstarlet.x86_64 \
    openssl-devel \
    glibc-devel \
    lz4 \
    lz4-devel \
    zstd \
    python2 \
    bzip2 \
    patch \
    which \
    perl \
    perl-Thread-Queue \
"

# Can be overriden at build time
ARG CI_RUNNER_PASSWORD=tuxbitbake


RUN set -e ;\
    # metadata for app stream
    cd /etc/yum.repos.d/ ;\
    sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* ;\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* ;\
    yum update -y -q ;\
    yum distribution-synchronization -y -q ;\
    yum install --assumeyes -q ${PKG_DEPS} ;\
    pip3 install awscli --upgrade --user ;\
    # to install rpcgen from powertools
    yum --enablerepo=powertools install rpcgen -y -q ;\
    # to install textinfo from powertools
    yum --enablerepo=powertools install texinfo -y -q ;\
    # Set default shell to bash
    #chsh -s /bin/bash | "" ;\
    # Set Python 2 as default
    alternatives --set python /usr/bin/python2 ;\
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
    yum clean expire-cache ;\
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
