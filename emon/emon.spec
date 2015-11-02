Name:		emon
Version:	0.1.0
Release:	1%{?dist}
Summary:	install and configure monitoring environment on clients

Group:		Applications
License:	Apache-2.0
URL:		https://github.com/henrysher/cob
Source0:	fetch-meta.sh
Source1:	emon-installer.sh
Source2:	rsyslog-local.conf
Source3:	rsyslog-remote.conf
Source4:	collectd.conf
Source5:	collectd-java.conf
Source6:	collectd-mysql.conf
Source7:	collectd-nginx.conf
Source8:	collectd-apache.conf
Source9:	collectd-glusterfs.conf
Source10:	collectd-activemq.conf
Source11:	carbon-c-relay.conf
Source12:	statsite.conf

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	collectd, collectd-disk, collectd-dns, collectd-lvm, collectd-netlink, collectd-ping, collectd-python, collectd-snmp, collectd-utils, collectd-curl_json, collectd-curl_xml, collectd-curl
Requires(pre):	carbon-c-relay
Requires(pre):	perl-Net-Amazon-EC2-Metadata
Requires:	statsite
AutoReqProv:    No

%description
The emon packages are used to install and configure monitoring on clients.
The metrics monitoring comprises of collectd, statsite and carbon-c-relay.
Rsyslog is configured to deliver logs to a remote rsyslog server.
AWS Instance metadata or a details file is used for configuration.
Without configuration the new services will not be started and configuration
changes will not be made to rsyslog.

%package java
Summary: emon-java pulls in additional resources for systems that run java
Group: Applications
Requires(pre): emon
Requires: collectd-java
%description java
Meta package to include resources not included by default in parent package

%package mysql
Summary: emon-mysql pulls in additional resources for systems that monitor mysql
Group: Applications
Requires(pre): emon
Requires: collectd-mysql, collectd-dbi
%description mysql
Meta package to include resources not included by default in parent package

%package nginx
Summary: emon-nginx pulls in additional resources for systems that run nginx
Group: Applications
Requires(pre): emon
Requires: collectd-nginx, collectd-curl
%description nginx
Meta package to include resources not included by default in parent package

%package apache
Summary: emon-apache pulls in additional resources for systems that run apache
Group: Applications
Requires(pre): emon
Requires: collectd-apache, collectd-curl
%description apache
Meta package to include resources not included by default in parent package

%package glusterfs
Summary: emon-glusterfs pulls in additional resources for systems that run glusterfs
Group: Applications
Requires(pre): emon
%description glusterfs
Meta package to include resources not included by default in parent package

%package activemq
Summary: emon-activemq pulls in additional resources for systems that run apache
Group: Applications
Requires(pre): emon
Requires: collectd-ampq
%description activemq
Meta package to include resources not included by default in parent package


%prep
#%setup -q
cp -p %SOURCE0 .
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


%build
exit 0

%install
rm -rf %{buildroot}
mkdir -vp %{buildroot}%{_sysconfdir}/emon
mkdir -vp %{buildroot}%{_sysconfdir}/collectd.d
mkdir -vp %{buildroot}%{_sysconfdir}/rsyslog.d
%{__install} -m 755 fetch-meta.sh %{buildroot}%{_sysconfdir}/emon/fetch-meta.sh
%{__install} -m 755 emon-installer.sh %{buildroot}%{_sysconfdir}/emon/emon-installer.sh
%{__install} -m 555 rsyslog-local.conf %{buildroot}%{_sysconfdir}/emon/rsyslog-local.conf
%{__install} -m 555 rsyslog-remote.conf %{buildroot}%{_sysconfdir}/emon/rsyslog-remote.conf
%{__install} -m 555 collectd.conf %{buildroot}%{_sysconfdir}/emon/collectd.conf
%{__install} -m 555 collectd-*.conf %{buildroot}%{_sysconfdir}/emon/
%{__install} -m 555 carbon-c-relay.conf %{buildroot}%{_sysconfdir}/emon/carbon-c-relay.conf
%{__install} -m 555 statsite.conf %{buildroot}%{_sysconfdir}/emon/statsite.conf


%clean
rm -rf %{buildroot}

%pre
exit 0

%post
exit 0

%pre java
exit 0

%post java
exit 0


%pre mysql
exit 0

%post mysql
exit 0


%pre nginx
exit 0

%post nginx
exit 0


%pre apache
exit 0

%post apache
exit 0


%pre glusterfs
exit 0

%post glusterfs
exit 0


%files
%defattr(-,root,root,-)
%attr(644, root, root) /etc/emon/collectd.conf
%attr(644, root, root) /etc/emon/carbon-c-relay.conf
%attr(644, root, root) /etc/emon/statsite.conf
%attr(644, root, root) /etc/emon/rsyslog-remote.conf
%attr(644, root, root) /etc/emon/rsyslog-local.conf
%attr(755, root, root) /etc/emon/emon-installer.sh
%attr(755, root, root) /etc/emon/fetch-meta.sh
%attr(644, root, root) /etc/emon/collectd-activemq.conf
%attr(644, root, root) /etc/emon/collectd-apache.conf
%attr(644, root, root) /etc/emon/collectd-glusterfs.conf
%attr(644, root, root) /etc/emon/collectd-mysql.conf
%attr(644, root, root) /etc/emon/collectd-java.conf
%attr(644, root, root) /etc/emon/collectd-nginx.conf

%files java

%files mysql

%files nginx

%files apache

%files glusterfs

%changelog
* Tue Sep 23 2015 Matthew Hollick <matthew@mayan-it.co.uk> 0.1.0-1
- First commit, not functional yet
- config file is empty
