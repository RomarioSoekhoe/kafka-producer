FROM docker.io/python:3.10.5-bullseye
# FROM docker.io/python:3.12.1-bullseye

# The user to use, defaulting to py (Python)
ARG user=appuser
ARG workdir=/home/${user}
# WORKDIR /home/appuser/app

ENV PYTHONPATH=${workdir}/app \
    PATH=$PATH:${workdir}/.local/bin \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ADD requirements.txt ./requirements.txt

# RUN python3 -m pip install pandas
RUN python -m pip install \
    --no-cache-dir \
#     --trusted-host pypi.python.org \
#     --trusted-host files.pythonhosted.org \
#     --trusted-host pypi.org \
    -r requirements.txt

COPY ./app ${workdir}/app

# Copy Schema's and Data to container
COPY ./schemas /schemas
COPY ./data /data

# Set timezone so the (python) logging has the proper timestamp
ENV TZ  Europe/Amsterdam


CMD ["python", "/home/appuser/app/main.py"]
