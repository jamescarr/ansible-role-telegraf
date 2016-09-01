distribution=ubuntu
version=14.04
init=/sbin/init

all: test

test:
	docker pull ${distribution}:${version}
	docker build --rm=true --file=tests/Dockerfile.${distribution}-${version} --tag=${distribution}-${version}:ansible tests
	distribution=${distribution} \
  init=${init} \
	version=${version} \
  run_opts="" \
	./run-tests.sh
