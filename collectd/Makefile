#!/usr/bin/make -f
#
# Some patching of the collectd directory name was neeed.
#
CWD=$(shell pwd -P)
BASE=${CWD}
NAME=collectd
SPEC=${NAME}.spec
VERSION="5.5"
FUDGE=".0"
DISTRO=eurostar-aws

rpm: srpm
	mock --root=$(BASE)/../$(DISTRO).cfg --no-clean --rebuild $(CWD)/SRPMS/*.src.rpm --resultdir=$(CWD)/../repo/
	mv $(BASE)/../repo/build.log $(BASE)/../repo/$(NAME)-rpm-build.log
	mv $(BASE)/../repo/root.log $(BASE)/../repo/$(NAME)-rpm-root.log
	mv $(BASE)/../repo/state.log $(BASE)/../repo/$(NAME)-rpm-state.log

srpm: prepare
	mock --root=$(BASE)/../$(DISTRO).cfg --buildsrpm --spec=$(CWD)/$(SPEC) --sources=$(CWD)/ --resultdir=$(CWD)/SRPMS

clean:
	@rm -rf RPMS SRPMS ${NAME}-${VERSION}${FUDGE} ${NAME}-${VERSION}${FUDGE}.tar.bz2

prepare: clean
	@mkdir -v SRPMS RPMS
	@git clone -b "${NAME}-${VERSION}" https://github.com/collectd/collectd.git
	@mv ${NAME} ${NAME}-${VERSION}${FUDGE}
	@tar -cvjf ${NAME}-${VERSION}${FUDGE}.tar.bz2 ${NAME}-${VERSION}${FUDGE}
	@rm -rf ${NAME}-${VERSION}${FUDGE}
