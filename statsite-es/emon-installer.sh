#!/bin/bash

SERVICES="carbon-c-relay collectd rsyslog statsite"
COLLECTD_CONF_FILES="collectd.conf"
CARBONRELAY_CONF_FILES="carbon-c-relay.conf"
RSYSLOG_CONF_FILES="rsyslog.local.conf rsyslog.remote.conf"
COLLECTD_GLUSTERFS_CONF_FILE="collectd-glusterfs.conf"
COLLECTD_TOMCAT_CONF_FILE="collectd-tomcat.conf"
COLLECTD_ACTIVEMQ_CONF_FILES="collectd-activemq.conf"
COLLECTD_MYSQL_CONF_FILES="collectd-mysql.conf"
COLLECTD_SPRING_CONF_FILES="collectd-spring.conf"
COLLECTD_APACHE_CONF_FILES="collectd-apache.conf"
CONF_FILES="${COLLECTD_CONF_FILES} ${CARBONRELAY_CONF_FILES} ${COLLECTD_GLUSTERFS_CONF_FILE} ${COLLECTD_TOMCAT_CONF_FILE} ${COLLECTD_ACTIVEMQ_CONF_FILES} ${COLLECTD_MYSQL_CONF_FILES} ${RSYSLOG_CONF_FILES} ${COLLECTD_SPRING_CONF_FILES} ${COLLECTD_APACHE_CONF_FILES}"
SVC_ACTION=0

for key in "$@"; do
  case $key in
    -r)
    SVC_ACTION=1
    shift
    ;;
    -s)
    SVC_ACTION=2
    shift
    ;;
    -S)
    SVC_ACTION=3
    shift
    ;;
    -h)
    echo "-r to restart, -s to start, -S to stop, -h for help"
    exit 0
    ;;
    *)
    ;;
  esac
done

cd /etc/eurostar

while read line; do 
  export ${line}
done </etc/eurostar/details

for file in ${CONF_FILES}; do
  cp ${file} ${file}.tmp
  sed -i "s/__SERVICE__/${service}/g" ${file}.tmp
  sed -i "s/__ENVIRONMENT__/${environment}/g" ${file}.tmp
  sed -i "s/__ROLE__/${role}/g" ${file}.tmp
  sed -i "s/__METRICSVR__/${metricshost}/g" ${file}.tmp
  sed -i "s/__LOGSVR__/${loghost}/g" ${file}.tmp
  sed -i "s/__HOSTNAME__/${HOSTNAME}/g" ${file}.tmp
  sed -i "s/__MYSQLHOST__/${mysqlhost}/g" ${file}.tmp
  sed -i "s/__MYSQLUSER__/${mysqluser}/g" ${file}.tmp
  sed -i "s/__MYSQLPASSWORD__/${mysqlpassword}/g" ${file}.tmp
  sed -i "s/__MYSQLDATABASE__/${mysqldatabase}/g" ${file}.tmp
done

cp -f carbon-c-relay.conf.tmp /etc/carbon-c-relay.conf
cp -f collectd.conf.tmp /etc/collectd.conf
cp -f rsyslog.remote.conf.tmp /etc/rsyslog.d/remote.conf
cp -f rsyslog.local.conf.tmp /etc/rsyslog.d/local.conf

if [ ! -z "${mysqlhost}" ]; then 
  cp -f collectd-mysql.conf.tmp /etc/collectd.d/mysql.conf
fi

if [ "${glusterfs}" = "true" ]; then
  cp -f collectd-glusterfs.conf.tmp /etc/collectd.d/glusterfs.conf
fi

if [ "${apache}" = "true" ]; then
  cp -f collectd-apache.conf.tmp /etc/collectd.d/apache.conf
fi

if [ "${tomcat}" = "true" ]; then
  cp -f collectd-tomcat.conf.tmp /etc/collectd.d/tomcat.conf
fi

if [ "${activemq}" = "true" ]; then
  cp -f collectd-activemq.conf.tmp /etc/collectd.d/activemq.conf
fi

if [ "${apache}" = "true" ]; then
  cp -f collectd-spring.conf.tmp /etc/collectd.d/spring.conf
fi

chmod -f 644 /etc/carbon-c-relay.conf /etc/collectd.conf /etc/rsyslog.d/remote.conf /etc/rsyslog.d/local.conf /etc/collectd.d/glusterfs.conf /etc/collectd.d/tomcat.conf /etc/collectd.d/activemq.conf /etc/collectd.d/mysql.conf

if [ "$(egrep -c '^\$IncludeConfig' /etc/rsyslog.conf)" -eq 0  ]; then echo '$IncludeConfig /etc/rsyslog.d/*.conf' >> /etc/ryslog.conf; fi


case ${SVC_ACTION} in
  0)
  echo "Configuration files updated, service states not changed"
  exit 0
  ;;
  1)
  for service in ${SERVICES}; do
    service ${service} restart
  done
  echo "Configuration files updated, services sent restart request"
  exit 0
  ;;
  2)
  for service in ${SERVICES}; do
    service ${service} start
  done
  echo "Configuration files updated, services sent start request"
  exit 0
  ;;
  3)
  for service in ${SERVICES}; do
    service ${service} stop
  done
  echo "Configuration files updated, services sent stop request"
  exit 0
  ;;
  *)
  echo "Out of cheese error"
  exit 1
  ;;
esac


#service=accounts
#environment=int
#role=appsvr
#metricshost=ec2-x.x.x.x
#loghost=ec2-y.y.y.y
#
#carbon-c-relay.conf:    __METRICSVR__:2003
#carbon-c-relay.conf:rewrite ^statsite\.(counts|timers)\.__SERVICE__\.(.*)
#carbon-c-relay.conf:  into aws.eu-west-1.__ENVIRONMENT__.__SERVICE__.hosts.__HOSTNAME__.\1
#rsyslog.remote.conf:template MyTemplate, "<%PRI%> %TIMESTAMP% Acc-Int-Cam01 %syslogtag%%msg% ::__SERVICE__:__ENVIRONMENT__:__ROLE__::\n"
#rsyslog.remote.conf:*.* @@__LOGSVR__:514
