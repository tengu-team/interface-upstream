


# Overview
This interface is used for charms who want to send upstream api information or set up a reverse-proxy gateway with NGINX.

# Usage
## Requires
By requiring the `upstream` interface, your charm is consuming one or more HTTP(S) servers, as a REST endpoint, to load-balance a set of servers, etc.

This interface layer will set the following states, as appropriate:
- `endpoint.{relation-name}.available` indicates that at least one upstream is connected. This state is automatically removed.
- `endpoint.{relation-name}.new-upstream` is set whenever a change happened in the connected upstreams. This is triggered when a providing charm sends new/updated info or when a relation departs. This state needs to be manually removed.

Use the `get_upstream()` method to get all upstream requests. It returns information in the following format:
```
[
    {
        'remote_unit_name': 'api/0',
        'nginx_config': '...'
    }
]
```
```python
@when('endpoint.{relation-name}.new-upstream')
def update_nginx_config():
    endpoint = get_endpoint_from_flag('endpoint.{endpoint-name}.available')
    upstreams = endpoint.get_upstream()
    clear_flag('endpoint.{relation-name}.new-upstream')
```


## Provides

By providing the `upstream` interface, your charm is providing upstream endpoints that can be load balanced, reverse-proxied. Use the `publish_info(nginx_config)` method to send NGINX configurations to the gateway.

This interface layer will set the following states, as appropriate:
- `endpoint.{relation-name}.available` indicates that at least one upstream is connected. This state is automatically removed.

```python
@when('endpoint.{endpoint-name}.available')
def configure():
    endpoint = get_endpoint_from_flag('endpoint.{endpoint-name}.available')
    nginx_config = "server { ..."
    endpoint.publish_info(nginx_config)
```


## Authors

This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab) of [Ghent University](https://www.ugent.be) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Sander Borny <sander.borny@ugent.be>

