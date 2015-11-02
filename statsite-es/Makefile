#!/usr/bin/make -f
#
#
CWD=$(shell pwd -P)
BASE=${CWD}
NAME=statsite
SPEC=${NAME}.spec
VERSION="0.7.1"
TAG="v${VERSION}"
DISTRO=eurostar-aws

rpm: srpm
	mock --root=$(BASE)/../$(DISTRO).cfg --no-clean --rebuild $(CWD)/SRPMS/*.src.rpm --resultdir=$(CWD)/../repo/
	mv $(BASE)/../repo/build.log $(BASE)/../repo/$(NAME)-rpm-build.log
	mv $(BASE)/../repo/root.log $(BASE)/../repo/$(NAME)-rpm-root.log
	mv $(BASE)/../repo/state.log $(BASE)/../repo/$(NAME)-rpm-state.log

srpm: prepare
	mock --root=$(BASE)/../$(DISTRO).cfg --buildsrpm --spec=$(CWD)/$(SPEC) --sources=$(CWD)/ --resultdir=$(CWD)/SRPMS

clean:
	@rm -rf RPMS SRPMS ${NAME} ${NAME}-${VERSION}.tar.bz2

prepare: clean
	@git clone --branch ${TAG} https://github.com/armon/statsite.git
	@cd ${NAME} && tar -cvzf ../${NAME}.tar.gz * && cd ..
