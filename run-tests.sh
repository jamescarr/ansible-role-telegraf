#!/bin/bash -eux

container_id=$(mktemp)

test_idempotence(){
  docker exec "$(cat ${container_id})" ansible-playbook /etc/ansible/roles/role_under_test/tests/test.yml \
    | grep -q 'changed=0.*failed=0' \
    && (echo 'Idempotence test: pass' && exit 0) \
    || (echo 'Idempotence test: fail' && exit 1)
}
# Run container in detached state
docker run --detach --volume="${PWD}":/etc/ansible/roles/role_under_test:ro ${run_opts} ${distribution}-${version}:ansible "${init}" > "${container_id}"

# Ansible syntax check.
docker exec --tty "$(cat ${container_id})" env TERM=xterm ansible-playbook /etc/ansible/roles/role_under_test/tests/test.yml --syntax-check

# Test role.
docker exec --tty "$(cat ${container_id})" env TERM=xterm ansible-playbook /etc/ansible/roles/role_under_test/tests/test.yml --skip-tags assertion

# Test role idempotence.
#test_idempotence()
# Ensure telegraf is installed.
docker exec --tty "$(cat ${container_id})" env TERM=xterm which telegraf

# Ensure it is started
docker exec --tty "$(cat ${container_id})" env TERM=xterm ansible-playbook /etc/ansible/roles/role_under_test/tests/test.yml --tags assertion

# Clean up
docker stop "$(cat ${container_id})"
