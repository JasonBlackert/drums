FROM debian:sid

WORKDIR /workspace/drums-mqtt

RUN apt-get update && apt-get install -qq \
        dpkg-dev \
        debhelper \
        dh-python \
        python3-all \
        pybuild-plugin-pyproject \
        python3-poetry-core \
        python3-pytest

CMD dpkg-buildpackage -b -rfakeroot -us -uc
