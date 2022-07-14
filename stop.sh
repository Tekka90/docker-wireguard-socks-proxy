#!/bin/sh
pid=$(ps | grep "sockd -D" | grep -v grep | head -1 | awk '{print $1}')
kill -9 $pid
sed -e "s/<connection>/eth0/" /etc/sockd.conf.template > /etc/sockd.conf
/usr/sbin/sockd -D