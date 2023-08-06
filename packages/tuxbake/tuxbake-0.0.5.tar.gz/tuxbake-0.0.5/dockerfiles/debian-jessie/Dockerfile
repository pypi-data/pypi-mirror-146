FROM debian:jessie

ENV DEBIAN_FRONTEND=noninteractive
ENV TOOLS_DIR=/home/tuxbitbake/tools
ENV PATH=${TOOLS_DIR}/bin:${PATH}
ENV LANG=en_US.UTF-8
ENV PKG_DEPS="\
    build-essential \
    chrpath \
    cpio \
    curl \
    diffstat \
    file \
    gawk \
    git \
    gnupg \
    iputils-ping \
    jq \
    less \
    locales \
    openssh-client \
    pigz \
    python3 \
    python3-pip \
    socat \
    sudo \
    texinfo \
    unzip \
    wget \
    xz-utils \
    xmlstarlet \
    awscli \
    libssl-dev \
    libc6-dev-i386 \
    liblz4-tool \
    #zstd \
    python \
"

# Can be overriden at build time
ARG CI_RUNNER_PASSWORD=tuxbitbake


RUN set -e ;\
    echo 'locales locales/locales_to_be_generated multiselect C.UTF-8 UTF-8, en_US.UTF-8 UTF-8 ' | debconf-set-selections ;\
    echo 'locales locales/default_environment_locale select en_US.UTF-8' | debconf-set-selections ;\
    echo 'dash dash/sh boolean false' | debconf-set-selections ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    # Set default shell to bash
    dpkg-reconfigure -p critical dash ;\
    # Set Python 3 as default
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
    # not implemented in debian:jessie
    #apt clean ;\
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
