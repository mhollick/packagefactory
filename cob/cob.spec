%define debug_package %{nil}

Name:		cob
Version:	2015.9.7
Release:	1%{?dist}
Summary:	s3 plugin for yum

Group:		Applications
License:	Apache-2.0
URL:		https://github.com/henrysher/cob
Source0:	cob.tar.gz
Source1:        cob.conf
Source2:        eurostar.repo
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description

Yet another yum S3 plugin, provides the way to accessing yum repository hosted on AWS S3.


%prep
#%setup -q
cp -p %SOURCE1 .
cp -p %SOURCE2 .

%build
exit 0

%install
rm -rf %{buildroot}
mkdir -vp %{buildroot}%{_sysconfdir}/yum.repos.d
mkdir -vp %{buildroot}%{_sysconfdir}/logrotate.d/
mkdir -vp %{buildroot}/usr/lib/yum-plugins/
mkdir -vp %{buildroot}%{_sysconfdir}/yum/pluginconf.d/
%{__install} -m 555 bosun.init %{buildroot}%{_sysconfdir}/init.d/bosun
%{__install} -m 444 bosun.conf %{buildroot}%{_sysconfdir}/bosun.conf

%clean
rm -rf %{buildroot}

%pre
exit 0

%files
%defattr(-,root,root,-)
%config /etc/bosun.conf
%attr(755, root, root) /etc/init.d/bosun
%attr(755, root, root) /usr/bin/bosun
%attr(644, bosun, root) /var/run/bosun

%changelog
* Wed Jul 15 2015 Matthew Hollick <matthew@mayan-it.co.uk> 0.3.0-1
- First commit, not functional yet
- config file is empty
