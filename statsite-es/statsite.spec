%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:		statsite
Version:	0.7.1
Release:	17%{?dist}
Summary:	A C implementation of statsd.
Group:		Applications
License:	See the LICENSE file.
URL:		https://github.com/armon/statsite
Source0:	statsite.tar.gz
Source1:        statsite.conf
Source2:        statsite.init
Source3:        collectd.conf
Source4:        rsyslog.remote.conf
Source5:        carbon-c-relay.conf
Source6:        emon-installer.sh
Source7:        rsyslog.local.conf
Source8:        collectd-activemq.conf
Source9:        collectd-apache.conf
Source10:       collectd-glusterfs.conf
Source11:       collectd-mysql.conf
Source12:       collectd-spring.conf
Source13:       collectd-tomcat.conf
Source14:       collectd-zeus.conf
Source15:       details.example


BuildRoot:      %{_tmppath}/%{name}-%{version}-root
#BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	scons
Requires(pre):	collectd-dns, collectd-netlink, collectd-curl_xml, collectd-memcachec, collectd-curl, carbon-c-relay
AutoReqProv:	No

%description

Statsite is a metrics aggregation server. Statsite is based heavily on Etsy's StatsD
https://github.com/etsy/statsd, and is wire compatible.

%prep
%setup -c %{name}-%{version}
cp -p %SOURCE1 .
cp -p %SOURCE2 .
cp -p %SOURCE3 .
cp -p %SOURCE4 .
cp -p %SOURCE5 .
cp -p %SOURCE6 .
cp -p %SOURCE7 .
cp -p %SOURCE8 .
cp -p %SOURCE9 .
cp -p %SOURCE10 .
cp -p %SOURCE11 .
cp -p %SOURCE12 .
cp -p %SOURCE13 .
cp -p %SOURCE14 .
cp -p %SOURCE15 .

%build
make %{?_smp_mflags}

%install
mkdir -vp $RPM_BUILD_ROOT/usr/bin
mkdir -vp $RPM_BUILD_ROOT/etc/init.d
mkdir -vp $RPM_BUILD_ROOT/etc/%{name}
mkdir -vp $RPM_BUILD_ROOT/etc/rsyslog.d
mkdir -vp $RPM_BUILD_ROOT/usr/libexec/%{name}
mkdir -vp $RPM_BUILD_ROOT/var/run/statsite
mkdir -vp $RPM_BUILD_ROOT/etc/eurostar
install -m 755 statsite $RPM_BUILD_ROOT/usr/bin
install -m 755 statsite.init $RPM_BUILD_ROOT/etc/init.d/statsite
install -m 644 statsite.conf $RPM_BUILD_ROOT/etc/%{name}/statsite.conf
install -m 644 collectd.conf $RPM_BUILD_ROOT/etc/eurostar/collectd.conf
install -m 644 carbon-c-relay.conf $RPM_BUILD_ROOT/etc/eurostar/carbon-c-relay.conf
install -m 644 rsyslog.remote.conf $RPM_BUILD_ROOT/etc/eurostar/rsyslog.remote.conf
install -m 644 rsyslog.local.conf $RPM_BUILD_ROOT/etc/eurostar/rsyslog.local.conf
install -m 755 emon-installer.sh $RPM_BUILD_ROOT/etc/eurostar/emon-installer.sh
install -m 644 collectd-activemq.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 collectd-apache.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 collectd-glusterfs.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 collectd-mysql.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 collectd-spring.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 collectd-tomcat.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 collectd-zeus.conf $RPM_BUILD_ROOT/etc/eurostar/
install -m 644 details.example $RPM_BUILD_ROOT/etc/eurostar/
cp -a sinks $RPM_BUILD_ROOT/usr/libexec/%{name}

%clean
make clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name}/ -c "Statsite aggregator daemon" %{name}

exit 0

%post
if [ "$1" = 1 ] ; then
	/sbin/chkconfig --add %{name}
	/sbin/chkconfig %{name} off
fi
chgrp %{name} %{_localstatedir}/run/%{name}
chmod 774 %{_localstatedir}/run/%{name}
/sbin/chkconfig --add %{name}

#Collectd does not create it's own user....
getent group collectd >/dev/null || groupadd -r collectd
getent passwd collectd >/dev/null || \
  useradd -r -g collectd -s /sbin/nologin \
    -d %{_localstatedir}/lib/collectd -c "Collectd Exec processes" collectd

/etc/eurostar/emon-installer.sh
service rsyslog restart
service carbon-c-relay restart
sleep 1
service statsite restart
service collectd restart
exit 0

%postun
if [ "$1" = 1 ] ; then
	/sbin/service %{name} restart
fi
exit 0

%preun
if [ "$1" = 0 ] ; then
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi
exit 0

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc CHANGELOG.md
%doc README.md
%config /etc/%{name}/statsite.conf
%attr(755, root, root) /usr/bin/statsite
%attr(755, root, root) /etc/init.d/statsite
%attr(644, root, root) /etc/eurostar/collectd.conf
%attr(644, root, root) /etc/eurostar/carbon-c-relay.conf
%attr(644, root, root) /etc/eurostar/rsyslog.remote.conf
%attr(644, root, root) /etc/eurostar/rsyslog.local.conf
%attr(755, root, root) /etc/eurostar/emon-installer.sh
%attr(644, root, root) /etc/eurostar/collectd-activemq.conf
%attr(644, root, root) /etc/eurostar/collectd-apache.conf
%attr(644, root, root) /etc/eurostar/collectd-glusterfs.conf
%attr(644, root, root) /etc/eurostar/collectd-mysql.conf
%attr(644, root, root) /etc/eurostar/collectd-spring.conf
%attr(644, root, root) /etc/eurostar/collectd-tomcat.conf
%attr(644, root, root) /etc/eurostar/collectd-zeus.conf
%attr(644, root, root) /etc/eurostar/details.example

%dir /usr/libexec/statsite
%dir /usr/libexec/statsite/sinks
%attr(755, root, root) /usr/libexec/statsite/sinks/__init__.py
%attr(755, root, root) /usr/libexec/statsite/sinks/binary_sink.py
%attr(755, root, root) /usr/libexec/statsite/sinks/librato.py
%attr(755, root, root) /usr/libexec/statsite/sinks/statsite_json_sink.rb
%attr(755, root, root) /usr/libexec/statsite/sinks/gmetric.py
%attr(755, root, root) /usr/libexec/statsite/sinks/influxdb.py
%attr(755, root, root) /usr/libexec/statsite/sinks/graphite.py
%attr(755, root, root) /usr/libexec/statsite/sinks/cloudwatch.sh
%attr(755, root, root) /usr/libexec/statsite/sinks/opentsdb.js
%attr(765, root, statsite) %{_localstatedir}/run/%{name}

%changelog
* Thu Aug 27 2015 Matthew Hollick <matthew@mayan-it.co.uk>
- Bastardised to get monitoring up and running quickly at Eurostar.
- Next version will revert back to vanilla, we just need our own repo first. :-/
- Graphite sink was missing.

* Fri Jul 18 2014 Gary Richardson <gary.richardson@gmail.com>
- added missing __init__.py to spec file
- fixed makefile for building RPMS

* Tue May 20 2014 Marcelo Teixeira Monteiro <marcelotmonteiro@gmail.com>
- Added initscript and config file
- small improvements

* Wed Nov 20 2013 Vito Laurenza <vitolaurenza@hotmail.com>
- Added 'sinks', which I overlooked initially.

* Fri Nov 15 2013 Vito Laurenza <vitolaurenza@hotmail.com>
- Initial release.
