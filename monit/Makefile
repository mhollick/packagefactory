#!/usr/bin/make -f
#
# 
#
CWD=$(shell pwd -P)
BASE=${CWD}
NAME=monit
SPEC=${NAME}.spec
VERSION="5.14"

rpm: srpm
	mock --no-clean --rebuild $(CWD)/SRPMS/*.src.rpm --resultdir=$(CWD)/RPMS/
	mv $(BASE)/../repo/build.log $(BASE)/../repo/$(NAME)-rpm-build.log
	mv $(BASE)/../repo/root.log $(BASE)/../repo/$(NAME)-rpm-root.log
	mv $(BASE)/../repo/state.log $(BASE)/../repo/$(NAME)-rpm-state.log

srpm: prepare
	mock --buildsrpm --spec=$(CWD)/$(SPEC) --sources=$(CWD)/ --resultdir=$(CWD)/SRPMS

clean:
	@rm -rf RPMS SRPMS ${NAME}-${VERSION}.tar.gz

prepare: clean
	@mkdir -v SRPMS RPMS
	@wget -c https://mmonit.com/monit/dist/${NAME}-${VERSION}.tar.gz
	#@git clone -b "${NAME}-${VERSION}" https://github.com/collectd/collectd.git
	#@mv ${NAME} ${NAME}-${VERSION}${FUDGE}
	#@tar -cvjf ${NAME}-${VERSION}${FUDGE}.tar.bz2 ${NAME}-${VERSION}${FUDGE}
	#@rm -rf ${NAME}-${VERSION}${FUDGE}
