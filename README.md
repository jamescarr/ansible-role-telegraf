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
      telegraf_render_config: true
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

This role also includes a module that you can use to add standalone
input/output configurations that are rendered under
`/etc/telegraf/conf.d`

```yaml
- name: Add file input
  telegraf_config:
  name: mcrouter
  plugins:
    input:
      tail:
        name_prefix: mcrouter_log
        from_beginning: true
        data_format: value
        data_type: string
        files:
          - /var/log/mcrouter/mcrouter.log
```

You can also specify a template for the config file if needed.

```yaml
- name: Add file input
  telegraf_config:
  name: mcrouter
  template: mcrouter.conf.j2

```

TODO: More examples using various inputs.


## License

MIT / BSD

## Author Information

This role was created in 2016 by [James Carr](http://blog.james-carr.org/).

