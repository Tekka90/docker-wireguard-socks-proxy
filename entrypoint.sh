#!/bin/sh

set -e
exec > /proc/1/fd/1

#ifname=$(basename $(ls -1 /etc/wireguard/*.conf | head -1) .conf)
#cp /etc/wireguard/$ifname.conf /tmp/wg.conf
#wg-quick up /tmp/wg.conf

if [ -z ${LOCAL_NETWORK} ]; then
    echo "Reroute will work only using localhost and from the host... To use outside, please set LOCAL_NETWORK env. variable."
else
    echo "Including network ${LOCAL_NETWORK} in the routing table" 
    gw=$(ip route | awk '/default/ {print $3}') 
    ip route add to ${LOCAL_NETWORK} via $gw dev eth0
fi

sed -e "s/<connection>/eth0/" /etc/sockd.conf.template > /etc/sockd.conf
/usr/sbin/sockd -D

python /app/webserver.py