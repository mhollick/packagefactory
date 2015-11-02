#!/usr/bin/make -f
#
# Some patching of the collectd directory name was neeed.
#
CWD=$(shell pwd -P)
BASE=${CWD}
NAME=librabbitmq
SPEC=${NAME}.spec
TAG="v0.7.0"
DISTRO=eurostar-aws

rpm: srpm
	mock --root=$(BASE)/../$(DISTRO).cfg --no-clean --rebuild $(CWD)/SRPMS/*.src.rpm --resultdir=$(CWD)/../repo/
	mv $(BASE)/../repo/build.log $(BASE)/../repo/$(NAME)-rpm-build.log
	mv $(BASE)/../repo/root.log $(BASE)/../repo/$(NAME)-rpm-root.log
	mv $(BASE)/../repo/state.log $(BASE)/../repo/$(NAME)-rpm-state.log

srpm: prepare
	mock --root=$(BASE)/../$(DISTRO).cfg --buildsrpm --spec=$(CWD)/$(SPEC) --sources=$(CWD)/ --resultdir=$(CWD)/SRPMS
	#rm -rf ${BASE}/carbon-c-relay

clean:
	@rm -rf RPMS SRPMS rabbitmq-c

prepare: clean
	@mkdir -v SRPMS RPMS
	@git clone -b "${TAG}" https://github.com/alanxz/rabbitmq-c.git
	@tar -cvjf rabbitmq-c-${TAG}.tar.gz rabbitmq-c
	@rm -rf rabbitmq-c
