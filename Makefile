DIRS = bosun carbon-c-relay collectd monit statsite-es
CMDSEP = ;
CWD=$(shell pwd -P)
BASE=${CWD}


all:
	$(foreach package, $(DIRS), cd $(BASE)/$(package) && make rpm $(CMDSEP))
	cd $(DIRS) && $(MAKE) rpm

.PHONY: bosun carbon-c-relay collectd monit statsite-es repo

bosun:
	cd bosun && $(MAKE) rpm

carbon-c-relay:
	cd carbon-c-relay && $(MAKE) rpm

collectd:
	cd collectd && $(MAKE) rpm

monit:
	cd monit && $(MAKE) rpm

statsite-es:
	cd statsite-es && $(MAKE) rpm

clean:
	@rm -rf */RPMS
	@rm -rf */SRPMS
	@rm -f */*gz
	@rm -f */*bz2

repo: all
	@mkdir -p repo
	$(foreach package, $(DIRS), cp $(package)/RPMS/*rpm repo/ $(CMDSEP))
	cd repo && createrepo .
