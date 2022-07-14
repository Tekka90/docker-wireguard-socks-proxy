# docker-wireguard-socks-proxy

Expose WireGuard as a SOCKS5 proxy in a Docker container.
In addition, create a webpage to be able to switch between the multiple connection available.

## What does this fork do?

Add capacity to handle multiple connection in one proxy + allow usage from outside the host

## Usage

A Simple `docker run` will do the trick:

```bash
docker run --rm --name wireguard-socks-proxy \
    --restart=unless-stopped \
    -e LOCAL_NETWORK=192.168.0.0/24 \
    --cap-add=NET_ADMIN \
    -v <location where are you wiregard.conf files>:/etc/wireguard/:ro \
    -p 12345:1080 \ #Port exposed for the Socket5 proxy
    -p 9180:8080 \ # Port exposed for the webinterface
    tekka90/docker-wireguard-socks-proxy:latest
```

Then connect to SOCKS proxy through through `127.0.0.1:12345` (or `ip of the host:12345` for Mac / docker-machine / etc.). For example:

```bash
curl --proxy socks5h://127.0.0.1:1080 ipinfo.io
curl --proxy socks5h://<host>:1080 ipinfo.io
```