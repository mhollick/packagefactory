#!/usr/bin/make -f
#
# Bosun
# AKA Dancing with Gophers
#
CWD=$(shell pwd -P)
BASE=${CWD}
NAME=cob
SPEC=${NAME}.spec
DISTRO=eurostar-aws

rpm: srpm
	mock --root=$(BASE)/../$(DISTRO).cfg --no-clean --rebuild $(CWD)/SRPMS/*.src.rpm --resultdir=$(CWD)/../repo/
	cp $(BASE)/../repo/build.log $(BASE)/../repo/$(NAME)-rpm-build.log
	cp $(BASE)/../repo/root.log $(BASE)/../repo/$(NAME)-rpm-root.log
	cp $(BASE)/../repo/state.log $(BASE)/../repo/$(NAME)-rpm-state.log

srpm: prepare
	mock --root=$(BASE)/../$(DISTRO).cfg --buildsrpm --spec=$(CWD)/$(SPEC) --sources=$(CWD)/ --resultdir=$(CWD)/SRPMS

clean:
	@rm -rf RPMS SRPMS 

prepare: clean
	git clone https://github.com/henrysher/cob.git
	tar cvzf cob.tar.gz cob
