#!/usr/bin/env bash

sed -i -e 's/LINO_FORWARD_INGEST_PROXY_0/${lino_forward_ingest_proxy_0}/g;s/LINO_FORWARD_INGEST_PROXY_1/${lino_forward_ingest_proxy_1}/g' /etc/haproxy/haproxy.cfg
echo "service haproxy restart(starting...)"
service haproxy restart
echo "service haproxy restart(completed)"