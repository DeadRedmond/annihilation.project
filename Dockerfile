FROM alpine:edge
LABEL Name=PerfectBot


# Add project source
WORKDIR /usr/src/PerfectBot
COPY . /usr/src/PerfectBot

# Update
RUN apk update && apk upgrade \
# Install dependencies
&& apk add --no-cache \
    git \
    ffmpeg \
    python3 \
    py3-pip \
    py3-yarl \
    py3-pynacl \
\
&& pip3 install --upgrade pip \
&& pip3 install wheel \
# Install pip dependencies
&& pip3 install --no-cache-dir -r requirements.txt

ENV DOCKER_ENV=true

ENTRYPOINT ["python3", "run.py"]