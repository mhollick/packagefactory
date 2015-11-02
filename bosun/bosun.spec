%define debug_package %{nil}

Name:		bosun	
Version:	2015.7.27
Release:	1%{?dist}
Summary:	An open-source, MIT licensed, monitoring and alerting system

Group:		Applications
License:	MIT
URL:		https://github.com/bosun-monitor/bosun
Source0:	go1.5.linux-amd64.tar.gz
Source1:        bosun.conf
Source2:        bosun.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	git wget
Requires(pre):	/usr/sbin/useradd
#Requires:	daemonize
Requires(post):	chkconfig

%description

Bosun is an open-source, MIT licensed, monitoring and alerting system by Stack Exchange. It has an expressive domain specific language for evaluating alerts and creating detailed notifications. It also lets you test your alerts against history for a faster development experience.

%prep
#%setup -q
cp -p %SOURCE0 .
cp -p %SOURCE1 .
cp -p %SOURCE2 .

%build
tar zxvf go1.5.linux-amd64.tar.gz
export GOROOT=$(pwd)/go
export PATH=${PATH}:${GOROOT}/bin
export GOPATH=$(pwd)
go get bosun.org/cmd/bosun
#gem install pleaserun
#/usr/local/bin/pleaserun --name bosun --user bosun --group bosun --description "Bosun is an alerting framework" --version "lsb-3.1" --platform sysv --verbose --overwrite --install-prefix $(pwd)  /usr/bin/bosun -c /etc/bosun.conf --prestart /usr/bin/bosun -r /etc/bosun.conf

%install
rm -rf %{buildroot}
mkdir -vp %{buildroot}%{_sysconfdir}/monit.d/
mkdir -vp %{buildroot}%{_sysconfdir}/logrotate.d/
mkdir -vp %{buildroot}%{_localstatedir}/run/%{name}
mkdir -vp %{buildroot}%{_bindir}
mkdir -vp %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 555 bin/bosun %{buildroot}%{_bindir}/%{name}
%{__install} -m 555 bosun.init %{buildroot}%{_sysconfdir}/init.d/bosun
%{__install} -m 444 bosun.conf %{buildroot}%{_sysconfdir}/bosun.conf

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name}/ -c "Bosun alerter" %{name}
exit 0

%files
%defattr(-,root,root,-)
%config /etc/bosun.conf
%attr(755, root, root) /etc/init.d/bosun
%attr(755, root, root) /usr/bin/bosun
%attr(644, bosun, root) /var/run/bosun

%changelog
* Wed Jul 15 2015 Matthew Hollick <matthew@mayan-it.co.uk> 0.3.0-1
- First Build
- config file is empty
