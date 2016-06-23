# Ansible Role: Telegraf

[![Build Status](https://travis-ci.org/jamescarr/ansible-role-telegraf.svg?branch=master)](https://travis-ci.org/jamescarr/ansible-role-telegraf)

Installs Telegraf on Debian/Ubuntu.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

## Dependencies

None.

## Example Playbook

Here's an example playbook using influxdb stats as an input and influxdb
as an output.

```yaml
    - hosts: utility
      vars_files:
        - vars/main.yml
      roles:
        - jamescarr.telegraf
          plugins:
            outputs:
              influxdb:
                urls:
                  - 'http://localhost:8086'
                database: telegraf
                precision: s
                retention_policy: default
                write_consistency: any
                timeout: 5s
            inputs:
              influxdb:
                urls: ['http://localhost:8086/debug/vars']

```

TODO: More examples using various inputs.


## License

MIT / BSD

## Author Information

This role was created in 2016 by [James Carr](http://blog.james-carr.org/).

