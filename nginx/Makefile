#!/usr/bin/make -f
#
# 
#
CWD=$(shell pwd -P)
BASE=${CWD}
NAME=nginx
SPEC=${NAME}.spec
NGINX_VERSION="1.8.0"
NAXSI_TAG="0.53-2"
NPS_VERSION="1.9.32.6"
NGINX_MORE_HEADERS_VERSION="0.261"
rpm: srpm
	@echo "Building RPM file"
	mock --no-clean --rebuild $(CWD)/SRPMS/*.src.rpm --resultdir=$(CWD)/RPMS/
	#mv $(BASE)/../repo/build.log $(BASE)/../repo/$(NAME)-rpm-build.log
	#mv $(BASE)/../repo/root.log $(BASE)/../repo/$(NAME)-rpm-root.log
	#mv $(BASE)/../repo/state.log $(BASE)/../repo/$(NAME)-rpm-state.log

srpm: prepare
	@echo "Building SRPM file"
	mock --buildsrpm --spec=$(CWD)/$(SPEC) --sources=$(CWD)/ --resultdir=$(CWD)/SRPMS

clean:
	@rm -rf RPMS SRPMS modules nginx-${NGINX_VERSION}.tar.gz modules.tar.gz

prepare: clean
	@mkdir -p SRPMS RPMS modules
	@echo "Downloading nginx source"
	@wget -qc http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
	@echo "Downloading naxsi WAF"
	@wget -qc https://github.com/nbs-system/naxsi/archive/${NAXSI_TAG}.tar.gz -O modules/naxsi-${NAXSI_TAG}.tar.gz
	@tar -C modules -zxf modules/naxsi-${NAXSI_TAG}.tar.gz && mv modules/naxsi-${NAXSI_TAG} modules/naxsi
	@rm -f modules/naxsi-${NAXSI_TAG}.tar.gz
	@echo "Downloading pagespeed for nginx"
	@wget -qc https://github.com/pagespeed/ngx_pagespeed/archive/release-${NPS_VERSION}-beta.zip -O modules/ngx_pagespeed-release-${NPS_VERSION}-beta.zip
	@cd modules && unzip -qq ngx_pagespeed-release-${NPS_VERSION}-beta.zip && mv ngx_pagespeed-release-${NPS_VERSION}-beta ngx_pagespeed
	@rm -f modules/ngx_pagespeed-release-${NPS_VERSION}-beta.zip
	@wget -qc https://dl.google.com/dl/page-speed/psol/${NPS_VERSION}.tar.gz -O modules/psol-${NPS_VERSION}.tar.gz
	@tar -C modules/ngx_pagespeed -zxf modules/psol-${NPS_VERSION}.tar.gz
	@rm -f modules/psol-${NPS_VERSION}.tar.gz
	@echo "Downloading StatsD for nginx"
	@cd modules && git clone --quiet https://github.com/zebrafishlabs/nginx-statsd.git
	@echo "Downloading upstream healthcheck for nginx (but not using)"
	@cd modules && git clone --quiet https://github.com/cep21/healthcheck_nginx_upstreams # needs to patch nginx so not building at the mo..
	@echo "Downloading improved headers module for nginx"
	@wget -qc https://github.com/openresty/headers-more-nginx-module/archive/v${NGINX_MORE_HEADERS_VERSION}.tar.gz -O modules/headers-more-nginx-module-v${NGINX_MORE_HEADERS_VERSION}.tar.gz
	@tar -C modules -zxf modules/headers-more-nginx-module-v${NGINX_MORE_HEADERS_VERSION}.tar.gz
	@rm -f modules/headers-more-nginx-module-v${NGINX_MORE_HEADERS_VERSION}.tar.gz
	@echo "Downloading substitutions filter for nginx"
	@cd modules && git clone --quiet git://github.com/yaoweibin/ngx_http_substitutions_filter_module.git
	@tar -czf modules.tar.gz modules
	@rm -rf modules
