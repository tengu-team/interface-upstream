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

from charms.reactive import when_any
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class UpstreamProvides(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def upstream_joined(self):
        set_flag(self.expand_name('available'))

    @when_any('endpoint.{endpoint_name}.departed')
    def upstream_departed(self):
        clear_flag(self.expand_name('available'))
        clear_flag(self.expand_name('departed'))

    def publish_info(self, nginx_config):
        for relation in self.relations:
            relation.to_publish['nginx_config'] = nginx_config
