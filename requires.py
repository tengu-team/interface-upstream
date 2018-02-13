#!/usr/bin/env python3
# Copyright (C) 2016  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from charms.reactive import when_any, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class UpstreamRequires(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def upstream_joined(self):
        set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def upstream_broken(self):
        clear_flag(self.expand_name('available'))

    @when_any('endpoint.{endpoint_name}.changed.nginx_config',
              'endpoint.{endpoint_name}.changed.location_config',
              'endpoint.{endpoint_name}.departed')
    def upstream_changed(self):
        set_flag(self.expand_name('new-upstream'))
        clear_flag(self.expand_name('changed.nginx_config'))
        clear_flag(self.expand_name('departed'))

    def get_nginx_configs(self):
        """
        [
            {
                'remote_unit_name': 'api/0',
                'nginx_config': 'server { ...'
            }
        ]
        """
        configs = []
        for relation in self.relations:
            for unit in relation.units:
                configs.append({
                    'remote_unit_name': unit.unit_name,
                    'nginx_config': unit.received['nginx_config'],
                })
        return configs

    def get_nginx_locations(self):
        """
        [
            {
                'remote_unit_name': 'api/0',
                'location_config': 'location / { ...'
            }
        ]
        """
        locations = []
        for relation in self.relations:
            for unit in relation.units:
                locations.append({
                    'remote_unit_name': unit.unit_name,
                    'location_config': unit.received['location_config']
                })
        return locations
