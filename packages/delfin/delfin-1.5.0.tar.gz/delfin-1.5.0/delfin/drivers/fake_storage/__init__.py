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
import copy
import random
import decorator

import math
import time

import six
from eventlet import greenthread
from oslo_config import cfg
from oslo_log import log
from oslo_utils import uuidutils

from delfin import exception, db
from delfin.common import constants
from delfin.drivers import driver

CONF = cfg.CONF

fake_opts = [
    cfg.StrOpt('fake_pool_range',
               default='1-100',
               help='The range of pool number for one device.'),
    cfg.StrOpt('fake_volume_range',
               default='1-2000',
               help='The range of volume number for one device.'),
    cfg.StrOpt('fake_api_time_range',
               default='0.1-0.5',
               help='The range of time cost for each API.'),
    cfg.StrOpt('fake_page_query_limit',
               default='500',
               help='The limitation of volumes for each query.'),
]

CONF.register_opts(fake_opts, "fake_driver")

LOG = log.getLogger(__name__)

MIN_WAIT, MAX_WAIT = 0.1, 0.5
MIN_POOL, MAX_POOL = 1, 100
MIN_PORTS, MAX_PORTS = 1, 10
MIN_DISK, MAX_DISK = 1, 100
MIN_VOLUME, MAX_VOLUME = 1, 2000
MIN_CONTROLLERS, MAX_CONTROLLERS = 1, 5
PAGE_LIMIT = 500
MIN_STORAGE, MAX_STORAGE = 1, 10
MIN_QUOTA, MAX_QUOTA = 1, 100
MIN_FS, MAX_FS = 1, 10
MIN_QTREE, MAX_QTREE = 1, 100
MIN_SHARE, MAX_SHARE = 1, 100
# Minimum sampling interval
MINIMUM_SAMPLE_DURATION_IN_MS = 60 * 1000
# count of instances for each resource type
RESOURCE_COUNT_DICT = {
    "storage": 1,
    "storagePool": MAX_POOL,
    "volume": MAX_VOLUME,
    "port": MAX_PORTS,
    "controller": MAX_CONTROLLERS,
    "disk": MAX_DISK,
    "filesystem": MAX_FS,
}

# Min and max are currently set to 1 to make sure at least one relation can be
# built in fake driver for host mapping elements
MIN_STORAGE_HOST_INITIATORS, MAX_STORAGE_HOST_INITIATORS = 1, 3
MIN_STORAGE_HOSTS, MAX_STORAGE_HOSTS = 1, 5
MIN_STORAGE_HOST_GROUPS, MAX_STORAGE_HOST_GROUPS = 1, 5
MIN_VOLUME_GROUPS, MAX_VOLUME_GROUPS = 1, 5
MIN_PORT_GROUPS, MAX_PORT_GROUPS = 1, 5
MAX_GROUP_RESOURCES_SIZE = 5
MIN_MASKING_VIEWS, MAX_MASKING_VIEWS = 1, 5
NON_GROUP_BASED_MASKING, GROUP_BASED_MASKING = 0, 1


def get_range_val(range_str, t):
    try:
        rng = range_str.split('-')
        if len(rng) != 2:
            raise exception.InvalidInput
        min_val = t(rng[0])
        max_val = t(rng[1])
        return min_val, max_val
    except Exception:
        LOG.error("Invalid range: {0}".format(range_str))
        raise exception.InvalidInput


def wait_random(low, high):
    @decorator.decorator
    def _wait(f, *a, **k):
        rd = random.randint(0, 100)
        secs = low + (high - low) * rd / 100
        greenthread.sleep(secs)
        return f(*a, **k)

    return _wait


class FakeStorageDriver(driver.StorageDriver):
    """FakeStorageDriver shows how to implement the StorageDriver,
    it also plays a role as faker to fake data for being tested by clients.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global MIN_WAIT, MAX_WAIT, MIN_POOL, MAX_POOL, MIN_VOLUME, MAX_VOLUME
        global PAGE_LIMIT
        MIN_WAIT, MAX_WAIT = get_range_val(
            CONF.fake_driver.fake_api_time_range, float)
        MIN_POOL, MAX_POOL = get_range_val(
            CONF.fake_driver.fake_pool_range, int)
        MIN_VOLUME, MAX_VOLUME = get_range_val(
            CONF.fake_driver.fake_volume_range, int)
        PAGE_LIMIT = int(CONF.fake_driver.fake_page_query_limit)
        self.rd_volumes_count = random.randint(MIN_VOLUME, MAX_VOLUME)
        self.rd_ports_count = random.randint(MIN_PORTS, MAX_PORTS)
        self.rd_storage_hosts_count = random.randint(MIN_STORAGE_HOSTS,
                                                     MAX_STORAGE_HOSTS)

    def _get_random_capacity(self):
        total = random.randint(1000, 2000)
        used = int(random.randint(0, 100) * total / 100)
        free = total - used
        return total, used, free

    def reset_connection(self, context, **kwargs):
        pass

    @wait_random(MIN_WAIT, MAX_WAIT)
    def get_storage(self, context):
        # Do something here

        sn = six.text_type(uuidutils.generate_uuid())
        try:
            # use existing sn if already registered storage
            storage = db.storage_get(context, self.storage_id)
            if storage:
                sn = storage['serial_number']
        except exception.StorageNotFound:
            LOG.debug('Registering new storage')
        except Exception:
            LOG.info('Error while retrieving storage from DB')
        total, used, free = self._get_random_capacity()
        raw = random.randint(2000, 3000)
        subscribed = random.randint(3000, 4000)
        return {
            'name': 'fake_driver',
            'description': 'fake driver.',
            'vendor': 'fake_vendor',
            'model': 'fake_model',
            'status': 'normal',
            'serial_number': sn,
            'firmware_version': '1.0.0',
            'location': 'HK',
            'total_capacity': total,
            'used_capacity': used,
            'free_capacity': free,
            'raw_capacity': raw,
            'subscribed_capacity': subscribed
        }

    @wait_random(MIN_WAIT, MAX_WAIT)
    def list_storage_pools(self, ctx):
        rd_pools_count = random.randint(MIN_POOL, MAX_POOL)
        LOG.info("###########fake_pools number for %s: %d" % (self.storage_id,
                                                              rd_pools_count))
        pool_list = []
        for idx in range(rd_pools_count):
            total, used, free = self._get_random_capacity()
            p = {
                "name": "storagePool_" + str(idx),
                "storage_id": self.storage_id,
                "native_storage_pool_id": "storagePool_" + str(idx),
                "description": "Fake Pool",
                "status": "normal",
                "total_capacity": total,
                "used_capacity": used,
                "free_capacity": free,
            }
            pool_list.append(p)
        return pool_list

    def list_volumes(self, ctx):
        # Get a random number as the volume count.
        rd_volumes_count = self.rd_volumes_count
        LOG.info("###########fake_volumes number for %s: %d" % (
            self.storage_id, rd_volumes_count))
        loops = math.ceil(rd_volumes_count / PAGE_LIMIT)
        volume_list = []
        for idx in range(loops):
            start = idx * PAGE_LIMIT
            end = (idx + 1) * PAGE_LIMIT
            if idx == (loops - 1):
                end = rd_volumes_count
            vs = self._get_volume_range(start, end)
            volume_list = volume_list + vs
        return volume_list

    def list_controllers(self, ctx):
        rd_controllers_count = random.randint(MIN_CONTROLLERS, MAX_CONTROLLERS)
        LOG.info("###########fake_controllers for %s: %d" %
                 (self.storage_id, rd_controllers_count))
        ctrl_list = []
        for idx in range(rd_controllers_count):
            total, used, free = self._get_random_capacity()
            cpu = ["Intel Xenon", "Intel Core ix", "ARM"]
            sts = list(constants.ControllerStatus.ALL)
            sts_len = len(constants.ControllerStatus.ALL) - 1
            c = {
                "name": "controller_" + str(idx),
                "storage_id": self.storage_id,
                "native_controller_id": "controller_" + str(idx),
                "location": "loc_" + str(random.randint(0, 99)),
                "status": sts[random.randint(0, sts_len)],
                "memory_size": total,
                "cpu_info": cpu[random.randint(0, 2)],
                "soft_version": "ver_" + str(random.randint(0, 999)),
            }
            ctrl_list.append(c)
        return ctrl_list

    def list_ports(self, ctx):
        rd_ports_count = self.rd_ports_count
        LOG.info("###########fake_ports for %s: %d" % (self.storage_id,
                                                       rd_ports_count))
        port_list = []
        for idx in range(rd_ports_count):
            max_s, normal, remain = self._get_random_capacity()
            conn_sts = list(constants.PortConnectionStatus.ALL)
            conn_sts_len = len(constants.PortConnectionStatus.ALL) - 1
            health_sts = list(constants.PortHealthStatus.ALL)
            health_sts_len = len(constants.PortHealthStatus.ALL) - 1
            port_type = list(constants.PortType.ALL)
            port_type_len = len(constants.PortType.ALL) - 1
            logic_type = list(constants.PortLogicalType.ALL)
            logic_type_len = len(constants.PortLogicalType.ALL) - 1
            c = {
                "name": "port_" + str(idx),
                "storage_id": self.storage_id,
                "native_port_id": "port_" + str(idx),
                "location": "location_" + str(random.randint(0, 99)),
                "connection_status": conn_sts[
                    random.randint(0, conn_sts_len)],
                "health_status": health_sts[
                    random.randint(0, health_sts_len)],
                "type": port_type[
                    random.randint(0, port_type_len)],
                "logical_type": logic_type[
                    random.randint(0, logic_type_len)],
                "speed": normal,
                "max_speed": max_s,
                "native_parent_id": "parent_id_" + str(random.randint(0, 99)),
                "wwn": "wwn_" + str(random.randint(0, 9999)),
                "mac_address": "mac_" + str(random.randint(0, 9999)),
                "ipv4": "0.0.0.0",
                "ipv4_mask": "255.255.255.0",
                "ipv6": "0",
                "ipv6_mask": "::",
            }
            port_list.append(c)
        return port_list

    def list_disks(self, ctx):
        rd_disks_count = random.randint(MIN_DISK, MAX_DISK)
        LOG.info("###########fake_disks for %s: %d" % (self.storage_id,
                                                       rd_disks_count))
        disk_list = []
        for idx in range(rd_disks_count):
            max_s, normal, remain = self._get_random_capacity()
            manufacturer = ["Intel", "Seagate", "WD", "Crucial", "HP"]
            sts = list(constants.DiskStatus.ALL)
            sts_len = len(constants.DiskStatus.ALL) - 1
            physical_type = list(constants.DiskPhysicalType.ALL)
            physical_type_len = len(constants.DiskPhysicalType.ALL) - 1
            logic_type = list(constants.DiskLogicalType.ALL)
            logic_type_len = len(constants.DiskLogicalType.ALL) - 1
            c = {
                "name": "disk_" + str(idx),
                "storage_id": self.storage_id,
                "native_disk_id": "disk_" + str(idx),
                "serial_number": "serial_" + str(random.randint(0, 9999)),
                "manufacturer": manufacturer[random.randint(0, 4)],
                "model": "model_" + str(random.randint(0, 9999)),
                "firmware": "firmware_" + str(random.randint(0, 9999)),
                "speed": normal,
                "capacity": max_s,
                "status": sts[random.randint(0, sts_len)],
                "physical_type": physical_type[
                    random.randint(0, physical_type_len)],
                "logical_type": logic_type[random.randint(0, logic_type_len)],
                "health_score": random.randint(0, 100),
                "native_diskgroup_id": "dg_id_" + str(random.randint(0, 99)),
                "location": "location_" + str(random.randint(0, 99)),
            }
            disk_list.append(c)
        return disk_list

    def list_quotas(self, ctx):
        rd_quotas_count = random.randint(MIN_QUOTA, MAX_QUOTA)
        LOG.info("###########fake_quotas for %s: %d"
                 % (self.storage_id, rd_quotas_count))
        quota_list = []
        for idx in range(rd_quotas_count):
            qtype = list(constants.QuotaType.ALL)
            qtype_len = len(constants.QuotaType.ALL) - 1
            max_cap = random.randint(1111, 9999)
            fslimit = random.randint(max_cap * 7, max_cap * 8)
            fhlimit = random.randint(max_cap * 8, max_cap * 9)
            slimit = random.randint(max_cap * 7000, max_cap * 8000)
            hlimit = random.randint(max_cap * 8000, max_cap * 9000)
            user_group = ['usr_', 'grp_']
            q = {
                "native_quota_id": "quota_" + str(idx),
                "type": qtype[random.randint(0, qtype_len)],
                "storage_id": self.storage_id,
                "native_filesystem_id": "quota_"
                                        + str(random.randint(0, 99)),
                "native_qtree_id": "qtree_"
                                   + str(random.randint(0, 99)),
                "capacity_hard_limit": hlimit,
                "capacity_soft_limit": slimit,
                "file_hard_limit": fhlimit,
                "file_soft_limit": fslimit,
                "file_count": random.randint(0, max_cap * 10),
                "used_capacity": random.randint(0, max_cap * 10000),
                "user_group_name": user_group[random.randint(0, 1)]
                                   + str(random.randint(0, 99)),
            }
            quota_list.append(q)
        return quota_list

    def list_filesystems(self, ctx):
        rd_filesystems_count = random.randint(MIN_FS, MAX_FS)
        LOG.info("###########fake_filesystems for %s: %d"
                 % (self.storage_id, rd_filesystems_count))
        filesystem_list = []
        for idx in range(rd_filesystems_count):
            total, used, free = self._get_random_capacity()
            boolean = [True, False]
            sts = list(constants.FilesystemStatus.ALL)
            sts_len = len(constants.FilesystemStatus.ALL) - 1
            worm = list(constants.WORMType.ALL)
            worm_len = len(constants.WORMType.ALL) - 1
            alloc_type = list(constants.VolumeType.ALL)
            alloc_type_len = len(constants.VolumeType.ALL) - 1
            security = list(constants.NASSecurityMode.ALL)
            security_len = len(constants.NASSecurityMode.ALL) - 1
            f = {
                "name": "filesystem_" + str(idx),
                "storage_id": self.storage_id,
                "native_filesystem_id": "filesystem_" + str(idx),
                "native_pool_id": "storagePool_" + str(idx),
                "status": sts[random.randint(0, sts_len)],
                "type": alloc_type[random.randint(0, alloc_type_len)],
                "security_mode": security[random.randint(0, security_len)],
                "total_capacity": total,
                "used_capacity": used,
                "free_capacity": free,
                "worm": worm[random.randint(0, worm_len)],
                "deduplicated": boolean[random.randint(0, 1)],
                "compressed": boolean[random.randint(0, 1)],
            }
            filesystem_list.append(f)
        return filesystem_list

    def list_qtrees(self, ctx):
        rd_qtrees_count = random.randint(MIN_QTREE, MAX_QTREE)
        LOG.info("###########fake_qtrees for %s: %d"
                 % (self.storage_id, rd_qtrees_count))
        qtree_list = []
        for idx in range(rd_qtrees_count):
            security = list(constants.NASSecurityMode.ALL)
            security_len = len(constants.NASSecurityMode.ALL) - 1

            t = {
                "name": "qtree_" + str(idx),
                "storage_id": self.storage_id,
                "native_qtree_id": "qtree_" + str(idx),
                "native_filesystem_id": "filesystem_"
                                        + str(random.randint(0, 99)),
                "security_mode": security[random.randint(0, security_len)],
                "path": "/path/qtree_" + str(random.randint(0, 99)),
            }
            qtree_list.append(t)

        return qtree_list

    def list_shares(self, ctx):
        rd_shares_count = random.randint(MIN_SHARE, MAX_SHARE)
        LOG.info("###########fake_shares for %s: %d"
                 % (self.storage_id, rd_shares_count))
        share_list = []
        for idx in range(rd_shares_count):
            pro = list(constants.ShareProtocol.ALL)
            pro_len = len(constants.ShareProtocol.ALL) - 1
            c = {
                "name": "share_" + str(idx),
                "storage_id": self.storage_id,
                "native_share_id": "share_" + str(idx),
                "native_filesystem_id": "filesystem_"
                                        + str(random.randint(0, 99)),
                "native_qtree_id": "qtree_"
                                   + str(random.randint(0, 99)),
                "protocol": pro[random.randint(0, pro_len)],
                "path": "/path/share_" + str(random.randint(0, 99)),
            }
            share_list.append(c)
        return share_list

    def add_trap_config(self, context, trap_config):
        pass

    def remove_trap_config(self, context, trap_config):
        pass

    @staticmethod
    def parse_alert(context, alert):
        pass

    def clear_alert(self, context, alert):
        pass

    def list_alerts(self, context, query_para=None):
        alert_list = [{
            "storage_id": self.storage_id,
            'alert_id': str(random.randint(1111111, 9999999)),
            'sequence_number': 100,
            'alert_name': 'SNMP connect failed',
            'category': 'Fault',
            'severity': 'Major',
            'type': 'OperationalViolation',
            'location': 'NetworkEntity=entity1',
            'description': "SNMP connection to the storage failed.",
            'recovery_advice': "Check snmp configurations.",
            'occur_time': int(time.time())
        }, {
            "storage_id": self.storage_id,
            'alert_id': str(random.randint(1111111, 9999999)),
            'sequence_number': 101,
            'alert_name': 'Link state down',
            'category': 'Fault',
            'severity': 'Critical',
            'type': 'CommunicationsAlarm',
            'location': 'NetworkEntity=entity2',
            'description': "Backend link has gone down",
            'recovery_advice': "Recheck the network configuration setting.",
            'occur_time': int(time.time())
        }, {
            "storage_id": self.storage_id,
            'alert_id': str(random.randint(1111111, 9999999)),
            'sequence_number': 102,
            'alert_name': 'Power failure',
            'category': 'Fault',
            'severity': 'Fatal',
            'type': 'OperationalViolation',
            'location': 'NetworkEntity=entity3',
            'description': "Power failure occurred. ",
            'recovery_advice': "Investigate power connection.",
            'occur_time': int(time.time())
        }, {
            "storage_id": self.storage_id,
            'alert_id': str(random.randint(1111111, 9999999)),
            'sequence_number': 103,
            'alert_name': 'Communication failure',
            'category': 'Fault',
            'severity': 'Critical',
            'type': 'CommunicationsAlarm',
            'location': 'NetworkEntity=network1',
            'description': "Communication link gone down",
            'recovery_advice': "Consult network administrator",
            'occur_time': int(time.time())
        }]
        return alert_list

    @wait_random(MIN_WAIT, MAX_WAIT)
    def _get_volume_range(self, start, end):
        volume_list = []

        for i in range(start, end):
            total, used, free = self._get_random_capacity()
            v = {
                "name": "volume_" + str(i),
                "storage_id": self.storage_id,
                "description": "Fake Volume",
                "status": "normal",
                "native_volume_id": "volume_" + str(i),
                "wwn": "fake_wwn_" + str(i),
                "total_capacity": total,
                "used_capacity": used,
                "free_capacity": free,
            }
            volume_list.append(v)
        return volume_list

    def _get_random_performance(self, metric_list, start_time, end_time):
        def get_random_timestamp_value():
            rtv = {}
            timestamp = start_time
            while timestamp < end_time:
                rtv[timestamp] = random.uniform(1, 100)
                timestamp += MINIMUM_SAMPLE_DURATION_IN_MS

            return rtv

        # The sample performance_params after filling looks like,
        # performance_params = {timestamp1: value1, timestamp2: value2}
        performance_params = {}
        for key in metric_list.keys():
            performance_params[key] = get_random_timestamp_value()
        return performance_params

    @wait_random(MIN_WAIT, MAX_WAIT)
    def get_resource_perf_metrics(self, storage_id, start_time, end_time,
                                  resource_type, metric_list):
        LOG.info("###########collecting metrics for resource %s: from"
                 " storage  %s" % (resource_type, self.storage_id))
        resource_metrics = []
        resource_count = RESOURCE_COUNT_DICT[resource_type]

        for i in range(resource_count):
            labels = {'storage_id': storage_id,
                      'resource_type': resource_type,
                      'resource_id': resource_type + '_' + str(i),
                      'type': 'RAW'}
            fake_metrics = self._get_random_performance(metric_list,
                                                        start_time, end_time)
            for key in metric_list.keys():
                labels['unit'] = metric_list[key]['unit']
                m = constants.metric_struct(name=key, labels=labels,
                                            values=fake_metrics[key])
                resource_metrics.append(copy.deepcopy(m))
        return resource_metrics

    @wait_random(MIN_WAIT, MAX_WAIT)
    def collect_perf_metrics(self, context, storage_id,
                             resource_metrics, start_time,
                             end_time):
        """Collects performance metric for the given interval"""
        merged_metrics = []
        for key in resource_metrics.keys():
            m = self.get_resource_perf_metrics(storage_id,
                                               start_time,
                                               end_time, key,
                                               resource_metrics[key])
            merged_metrics += m
        return merged_metrics

    @staticmethod
    def get_capabilities(context, filters=None):
        """Get capability of supported driver"""
        return {
            'is_historic': False,
            'performance_metric_retention_window': 4500,
            'resource_metrics': {
                "storage": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Represents how much data is "
                                       "successfully transferred in MB/s"
                    },
                    "responseTime": {
                        "unit": "ms",
                        "description": "Average time taken for an IO "
                                       "operation in ms"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Input/output operations per second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Represents how much data read is "
                                       "successfully transferred in MB/s"
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Represents how much data write is "
                                       "successfully transferred in MB/s"
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read requests per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write requests per second"
                    },
                },
                "storagePool": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Total data transferred per second "
                    },
                    "responseTime": {
                        "unit": "ms",
                        "description": "Average time taken for an IO "
                                       "operation"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Read and write operations per second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Total read data transferred per"
                                       " second"
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Total write data transferred per"
                                       " second "
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read operations per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write operations per second"
                    },

                },
                "volume": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Total data transferred per second "
                    },
                    "responseTime": {
                        "unit": "ms",
                        "description": "Average time taken for an IO "
                                       "operation"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Read and write  operations per"
                                       " second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Total read data transferred per "
                                       "second "
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Total write data transferred per"
                                       " second "
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read operations per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write operations per second"
                    },
                    "cacheHitRatio": {
                        "unit": "%",
                        "description": "Percentage of io that are cache "
                                       "hits"
                    },
                    "readCacheHitRatio": {
                        "unit": "%",
                        "description": "Percentage of read ops that are cache"
                                       " hits"
                    },
                    "writeCacheHitRatio": {
                        "unit": "%",
                        "description": "Percentage of write ops that are cache"
                                       " hits"
                    },
                    "ioSize": {
                        "unit": "KB",
                        "description": "The average size of IO requests in KB"
                    },
                    "readIoSize": {
                        "unit": "KB",
                        "description": "The average size of read IO requests "
                                       "in KB."
                    },
                    "writeIoSize": {
                        "unit": "KB",
                        "description": "The average size of read IO requests"
                                       " in KB."
                    },
                },
                "controller": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Total data transferred per second "
                    },
                    "responseTime": {
                        "unit": "ms",
                        "description": "Average time taken for an IO "
                                       "operation"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Read and write  operations per "
                                       "second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Total read data transferred per "
                                       "second "
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Total write data transferred per "
                                       "second "
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read operations per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write operations per second"
                    },

                },
                "port": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Total data transferred per second "
                    },
                    "responseTime": {
                        "unit": "ms",
                        "description": "Average time taken for an IO "
                                       "operation"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Read and write  operations per "
                                       "second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Total read data transferred per "
                                       "second "
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Total write data transferred per "
                                       "second "
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read operations per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write operations per second"
                    },

                },
                "disk": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Total data transferred per second "
                    },
                    "responseTime": {
                        "unit": "ms",
                        "description": "Average time taken for an IO "
                                       "operation"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Read and write  operations per"
                                       " second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Total read data transferred per"
                                       " second "
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Total write data transferred per"
                                       " second "
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read operations per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write operations per second"
                    },

                },
                "filesystem": {
                    "throughput": {
                        "unit": "MB/s",
                        "description": "Total data transferred per second "
                    },
                    "readResponseTime": {
                        "unit": "ms",
                        "description": "Average time taken for a read"
                                       "operation"
                    },
                    "writeResponseTime": {
                        "unit": "ms",
                        "description": "Average time taken for a write "
                                       "operation"
                    },
                    "iops": {
                        "unit": "IOPS",
                        "description": "Read and write  operations per"
                                       " second"
                    },
                    "readThroughput": {
                        "unit": "MB/s",
                        "description": "Total read data transferred per "
                                       "second "
                    },
                    "writeThroughput": {
                        "unit": "MB/s",
                        "description": "Total write data transferred per"
                                       " second "
                    },
                    "readIops": {
                        "unit": "IOPS",
                        "description": "Read operations per second"
                    },
                    "writeIops": {
                        "unit": "IOPS",
                        "description": "Write operations per second"
                    },
                    "readIoSize": {
                        "unit": "KB",
                        "description": "The average size of read IO requests "
                                       "in KB."
                    },
                    "writeIoSize": {
                        "unit": "KB",
                        "description": "The average size of read IO requests"
                                       " in KB."
                    },
                },

            }

        }

    def list_storage_host_initiators(self, ctx):
        rd_storage_host_initiators_count = random.randint(
            MIN_STORAGE_HOST_INITIATORS, MAX_STORAGE_HOST_INITIATORS)
        LOG.info("###########fake_storage_host_initiators for %s: %d"
                 % (self.storage_id, rd_storage_host_initiators_count))
        storage_host_initiators_list = []
        for idx in range(rd_storage_host_initiators_count):
            f = {
                "name": "storage_host_initiator_" + str(idx),
                "description": "storage_host_initiator_" + str(idx),
                "alias": "storage_host_initiator_" + str(idx),
                "storage_id": self.storage_id,
                "native_storage_host_initiator_id":
                    "storage_host_initiator_" + str(idx),
                "wwn": "wwn_" + str(idx),
                "status": "Normal",
                "native_storage_host_id": "storage_host_" + str(idx),
            }
            storage_host_initiators_list.append(f)
        return storage_host_initiators_list

    def list_storage_hosts(self, ctx):
        rd_storage_hosts_count = self.rd_storage_hosts_count
        LOG.info("###########fake_storage_hosts for %s: %d"
                 % (self.storage_id, rd_storage_hosts_count))
        storage_host_list = []
        for idx in range(rd_storage_hosts_count):
            f = {
                "name": "storage_host_" + str(idx),
                "description": "storage_host_" + str(idx),
                "storage_id": self.storage_id,
                "native_storage_host_id": "storage_host_" + str(idx),
                "os_type": "linux",
                "status": "Normal",
                "ip_address": "1.2.3." + str(idx)
            }
            storage_host_list.append(f)
        return storage_host_list

    def list_storage_host_groups(self, ctx):
        rd_storage_host_groups_count = random.randint(
            MIN_STORAGE_HOST_GROUPS, MAX_STORAGE_HOST_GROUPS)
        LOG.info("###########fake_storage_host_groups for %s: %d"
                 % (self.storage_id, rd_storage_host_groups_count))
        storage_host_grp_list = []
        for idx in range(rd_storage_host_groups_count):
            # Create hosts in hosts group
            host_name_list = []
            storage_hosts_count = self.rd_storage_hosts_count - 1
            if storage_hosts_count > 0:
                for i in range(MAX_GROUP_RESOURCES_SIZE):
                    host_name = "storage_host_" + str(
                        random.randint(0, storage_hosts_count))
                    if host_name not in host_name_list:
                        host_name_list.append(host_name)

            # Create comma separated list
            storage_hosts = None
            for host in host_name_list:
                if storage_hosts:
                    storage_hosts = storage_hosts + "," + host
                else:
                    storage_hosts = host

            f = {
                "name": "storage_host_group_" + str(idx),
                "description": "storage_host_group_" + str(idx),
                "storage_id": self.storage_id,
                "native_storage_host_group_id": "storage_host_group_"
                                                + str(idx),
                "storage_hosts": storage_hosts
            }
            storage_host_grp_list.append(f)
        return storage_host_grp_list

    def list_port_groups(self, ctx):
        rd_port_groups_count = random.randint(MIN_PORT_GROUPS,
                                              MAX_PORT_GROUPS)
        LOG.info("###########fake_port_groups for %s: %d"
                 % (self.storage_id, rd_port_groups_count))
        port_grp_list = []
        for idx in range(rd_port_groups_count):
            # Create ports in ports group
            port_name_list = []
            ports_count = self.rd_ports_count - 1
            if ports_count > 0:
                for i in range(MAX_GROUP_RESOURCES_SIZE):
                    port_name = "port_" + str(
                        random.randint(0, ports_count))
                    if port_name not in port_name_list:
                        port_name_list.append(port_name)

            # Create comma separated list
            ports = None
            for port in port_name_list:
                if ports:
                    ports = ports + "," + port
                else:
                    ports = port

            f = {
                "name": "port_group_" + str(idx),
                "description": "port_group_" + str(idx),
                "storage_id": self.storage_id,
                "native_port_group_id": "port_group_" + str(idx),
                "ports": ports
            }

            port_grp_list.append(f)
        return port_grp_list

    def list_volume_groups(self, ctx):
        rd_volume_groups_count = random.randint(MIN_VOLUME_GROUPS,
                                                MAX_VOLUME_GROUPS)
        LOG.info("###########fake_volume_groups for %s: %d"
                 % (self.storage_id, rd_volume_groups_count))
        volume_grp_list = []
        for idx in range(rd_volume_groups_count):
            # Create volumes in volumes group
            volume_name_list = []
            volumes_count = self.rd_volumes_count - 1
            if volumes_count > 0:
                for i in range(MAX_GROUP_RESOURCES_SIZE):
                    volume_name = "volume_" + str(
                        random.randint(0, volumes_count))
                    if volume_name not in volume_name_list:
                        volume_name_list.append(volume_name)

            # Create comma separated list
            volumes = None
            for volume in volume_name_list:
                if volumes:
                    volumes = volumes + "," + volume
                else:
                    volumes = volume

            f = {
                "name": "volume_group_" + str(idx),
                "description": "volume_group_" + str(idx),
                "storage_id": self.storage_id,
                "native_volume_group_id": "volume_group_" + str(idx),
                "volumes": volumes
            }
            volume_grp_list.append(f)
        return volume_grp_list

    def list_masking_views(self, ctx):
        rd_masking_views_count = random.randint(MIN_MASKING_VIEWS,
                                                MAX_MASKING_VIEWS)
        LOG.info("##########fake_masking_views for %s: %d"
                 % (self.storage_id, rd_masking_views_count))
        masking_view_list = []

        for idx in range(rd_masking_views_count):
            is_group_based = random.randint(NON_GROUP_BASED_MASKING,
                                            GROUP_BASED_MASKING)
            if is_group_based:
                native_storage_host_group_id = "storage_host_group_" + str(idx)
                native_volume_group_id = "volume_group_" + str(idx)
                native_port_group_id = "port_group_" + str(idx)
                native_storage_host_id = ""
                native_volume_id = ""
                native_port_id = ""

            else:
                native_storage_host_group_id = ""
                native_volume_group_id = ""
                native_port_group_id = ""
                native_storage_host_id = "storage_host_" + str(idx)
                native_volume_id = "volume_" + str(idx)
                native_port_id = "port_" + str(idx)

            f = {
                "name": "masking_view_" + str(idx),
                "description": "masking_view_" + str(idx),
                "storage_id": self.storage_id,
                "native_masking_view_id": "masking_view_" + str(idx),
                "native_storage_host_group_id": native_storage_host_group_id,
                "native_volume_group_id": native_volume_group_id,
                "native_port_group_id": native_port_group_id,
                "native_storage_host_id": native_storage_host_id,
                "native_volume_id": native_volume_id,
                "native_port_id": native_port_id
            }
            masking_view_list.append(f)
        return masking_view_list
