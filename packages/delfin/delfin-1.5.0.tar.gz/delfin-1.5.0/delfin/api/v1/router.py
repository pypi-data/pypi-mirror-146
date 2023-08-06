# Copyright 2020 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from delfin.api import common
from delfin.api import extensions
from delfin.api.v1 import access_info
from delfin.api.v1 import alert_source
from delfin.api.v1 import alerts
from delfin.api.v1 import controllers
from delfin.api.v1 import disks
from delfin.api.v1 import filesystems
from delfin.api.v1 import ports
from delfin.api.v1 import qtrees
from delfin.api.v1 import quotas
from delfin.api.v1 import shares
from delfin.api.v1 import storage_pools
from delfin.api.v1 import storages
from delfin.api.v1 import volumes
from delfin.api.v1 import storage_hosts
from delfin.api.v1 import storage_host_initiators
from delfin.api.v1 import storage_host_groups
from delfin.api.v1 import port_groups
from delfin.api.v1 import volume_groups
from delfin.api.v1 import masking_views


class APIRouter(common.APIRouter):

    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper):
        mapper.redirect("", "/")

        self.resources['storages'] = storages.create_resource()
        mapper.resource("storage", "storages",
                        controller=self.resources['storages'],
                        member={'sync': 'POST'})

        mapper.connect("storages", "/storages/sync",
                       controller=self.resources['storages'],
                       action="sync_all",
                       conditions={"method": ["POST"]})

        mapper.connect("storages", "/storages/{id}/capabilities",
                       controller=self.resources['storages'],
                       action="get_capabilities",
                       conditions={"method": ["GET"]})

        self.resources['access_info'] = access_info.create_resource()
        mapper.connect("storages", "/storages/{id}/access-info",
                       controller=self.resources['access_info'],
                       action="show",
                       conditions={"method": ["GET"]})

        mapper.connect("storages", "/storages/{id}/access-info",
                       controller=self.resources['access_info'],
                       action="update",
                       conditions={"method": ["PUT"]})

        mapper.connect("storages", "/access-infos",
                       controller=self.resources['access_info'],
                       action="show_all",
                       conditions={"method": ["GET"]})

        self.resources['alert_sources'] = alert_source.create_resource()
        mapper.connect("storages", "/storages/{id}/snmp-config",
                       controller=self.resources['alert_sources'],
                       action="put",
                       conditions={"method": ["PUT"]})
        mapper.connect("storages", "/storages/{id}/snmp-config",
                       controller=self.resources['alert_sources'],
                       action="show",
                       conditions={"method": ["GET"]})
        mapper.connect("storages", "/storages/{id}/snmp-config",
                       controller=self.resources['alert_sources'],
                       action="delete",
                       conditions={"method": ["DELETE"]})
        mapper.connect("storages", "/snmp-configs",
                       controller=self.resources['alert_sources'],
                       action="show_all",
                       conditions={"method": ["GET"]})

        self.resources['alerts'] = alerts.create_resource()
        mapper.connect("storages", "/storages/{id}/alerts/{sequence_number}",
                       controller=self.resources['alerts'],
                       action="delete",
                       conditions={"method": ["DELETE"]})

        mapper.connect("storages", "/storages/{id}/alerts",
                       controller=self.resources['alerts'],
                       action="show",
                       conditions={"method": ["GET"]})

        mapper.connect("storages", "/storages/{id}/alerts/sync",
                       controller=self.resources['alerts'],
                       action="sync",
                       conditions={"method": ["POST"]})

        self.resources['storage-pools'] = storage_pools.create_resource()
        mapper.resource("storage-pool", "storage-pools",
                        controller=self.resources['storage-pools'])

        self.resources['volumes'] = volumes.create_resource()
        mapper.resource("volume", "volumes",
                        controller=self.resources['volumes'])

        self.resources['controllers'] = controllers.create_resource()
        mapper.resource("controller", "controllers",
                        controller=self.resources['controllers'])

        self.resources['ports'] = ports.create_resource()
        mapper.resource("port", "ports",
                        controller=self.resources['ports'])

        self.resources['disks'] = disks.create_resource()
        mapper.resource("disk", "disks",
                        controller=self.resources['disks'])

        self.resources['filesystems'] = filesystems.create_resource()
        mapper.resource("filesystems", "filesystems",
                        controller=self.resources['filesystems'])

        self.resources['qtrees'] = qtrees.create_resource()
        mapper.resource("qtrees", "qtrees",
                        controller=self.resources['qtrees'])

        self.resources['quotas'] = quotas.create_resource()
        mapper.resource("quotas", "quotas",
                        controller=self.resources['quotas'])

        self.resources['shares'] = shares.create_resource()
        mapper.resource("shares", "shares",
                        controller=self.resources['shares'])

        self.resources['storage_host_initiators'] \
            = storage_host_initiators.create_resource()
        mapper.connect("storages", "/storages/{id}/storage-host-initiators",
                       controller=self.resources['storage_host_initiators'],
                       action="show",
                       conditions={"method": ["GET"]})

        self.resources['storage_hosts'] = storage_hosts.create_resource()
        mapper.connect("storages", "/storages/{id}/storage-hosts",
                       controller=self.resources['storage_hosts'],
                       action="show",
                       conditions={"method": ["GET"]})

        self.resources['storage_host_groups'] \
            = storage_host_groups.create_resource()
        mapper.connect("storages", "/storages/{id}/storage-host-groups",
                       controller=self.resources['storage_host_groups'],
                       action="show",
                       conditions={"method": ["GET"]})

        self.resources['port_groups'] \
            = port_groups.create_resource()
        mapper.connect("storages", "/storages/{id}/port-groups",
                       controller=self.resources['port_groups'],
                       action="show",
                       conditions={"method": ["GET"]})

        self.resources['volume_groups'] \
            = volume_groups.create_resource()
        mapper.connect("storages", "/storages/{id}/volume-groups",
                       controller=self.resources['volume_groups'],
                       action="show",
                       conditions={"method": ["GET"]})

        self.resources['masking_views'] \
            = masking_views.create_resource()
        mapper.connect("storages", "/storages/{id}/masking-views",
                       controller=self.resources['masking_views'],
                       action="show",
                       conditions={"method": ["GET"]})
