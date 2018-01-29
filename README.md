

# Overview
This interface is used for charms who want to send upstream api information or set up a reverse-proxy gateway.

# Usage
## Requires
By requiring the `upstream` interface, your charm is consuming one or more HTTP(S) servers, as a REST endpoint, to load-balance a set of servers, etc.

The `endpoint.{relation-name}.available` flag indicates that at least one upstream is connected. Use the `get_upstream()` method to get all upstream requests. It returns information in the following format:
```
[
    {
        'remote_unit_name': 'api/0',
        'vhost': '...'
    }
]
```

## Provides

By providing the `upstream` interface, your charm is providing upstream endpoints that can be load balanced, reverse-proxied. Use the `publish_info(vhost)` method to send configurations to the gateway.

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

