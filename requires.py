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

    @when_any('endpoint.{endpoint_name}.departed')
    def upstream_departed(self):
        if self.relations:
            set_flag(self.expand_name('new-upstream'))
        else:
            set_flag(self.expand_name('cleanup'))
            clear_flag(self.expand_name('available'))
        clear_flag(self.expand_name('departed'))

    @when_any('endpoint.{endpoint_name}.changed.nginx_config')
    def upstream_changed(self):
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-upstream'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.nginx_config'))

    def get_upstreams(self):
        """
        [
            {
                'remote_unit_name': 'api/0',
                'nginx_config': 'server { ...'
            }
        ]         
        """
        upstreams = []
        for relation in self.relations:
            for unit in relation.units:
                upstreams.append({
                    'remote_unit_name': unit.unit_name,
                    'nginx_config': unit.received['nginx_config'],
                })
        return upstreams
