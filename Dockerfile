# Expose a WireGuard connection as SOCKS5 proxy
#
# Using alpine 3.10 becasue of wireguard issue with earlier version. Need to add 3.12 for dante-server

FROM python:alpine3.10

RUN apk update && apk add --update-cache wireguard-tools openresolv ip6tables iptables \
  && rm -rf /var/cache/apk/* \
  && pip install json2html

RUN printf "https://dl-3.alpinelinux.org/alpine/v3.12/main\nhttps://dl-3.alpinelinux.org/alpine/v3.12/community" > /etc/apk/repositories \
    && apk update && apk add dante-server

COPY ./sockd.conf.template /etc/
COPY ./entrypoint.sh /entrypoint.sh
COPY ./start.sh ./stop.sh /app/
COPY ./*.py /app/
COPY ./icon/* /app/icon/
RUN chmod +rwx /entrypoint.sh

ENV LOCAL_NETWORK=

ENTRYPOINT "/entrypoint.sh"
