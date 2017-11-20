FROM memcached:1.5-alpine

USER root
RUN apk update
RUN apk add cyrus-sasl
RUN echo "847gns0o3t983zdpovzfnmsaf4g4328743njewfg" | saslpasswd2 -p -a memcached -u memcached -c cacheuser
RUN chmod 777 /etc/sasldb2
USER memcache

CMD ["memcached", "-S"]