# Copyright 2021 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time

from oslo_log import log

from delfin.common import constants
from delfin.drivers.netapp.dataontap import constants as constant
from delfin.drivers.utils.tools import Tools

LOG = log.getLogger(__name__)


class PerformanceHandler(object):
    TIME_TYPE = '%Y-%m-%dT%H:%M:%SZ'

    @staticmethod
    def get_value(value, key):
        if key == 'iops' or key == 'readIops' or key == 'writeIops':
            return int(value)
        elif key == 'throughput' or key == 'readThroughput' \
                or key == 'writeThroughput':
            unit = constant.CAP_MAP[key]['unit']
            return PerformanceHandler.get_unit_size(value, unit)
        elif key == 'responseTime':
            return round(int(value) / 1000, 3)
        else:
            return value

    @staticmethod
    def get_unit_size(value, unit):
        if value is None:
            return None
        if value == '0' or value == 0:
            return 0
        unit_array = unit.split('/')
        capacity = Tools.change_capacity_to_bytes(unit_array[0])
        if capacity == 1:
            return value
        return round(int(value) / capacity, 3)

    @staticmethod
    def get_perf_value(metrics, storage_id, start_time, end_time,
                       data_info, resource_id, resource_name, resource_type):
        fs_metrics = []
        selection = metrics.get(resource_type)
        for key in selection:
            labels = {
                'storage_id': storage_id,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'resource_name': resource_name,
                'type': 'RAW',
                'unit': constant.CAP_MAP[key]['unit']
            }
            values = {}
            for perf_info in data_info:
                if perf_info.get('timestamp'):
                    occur_time = \
                        int(time.mktime(time.strptime(
                            perf_info.get('timestamp'),
                            PerformanceHandler.TIME_TYPE)))
                    second_offset = \
                        (time.mktime(time.localtime()) -
                         time.mktime(time.gmtime()))
                    timestamp = \
                        (occur_time + int(second_offset)) * 1000
                    if int(start_time) <= timestamp <= int(end_time) \
                            and timestamp % 60000 == 0:
                        key_list = constant.PERF_MAP.get(key, [])
                        if len(key_list) > 0:
                            value = perf_info.get(key_list[0], {}) \
                                .get(key_list[1], None)
                            if value is not None:
                                value = PerformanceHandler. \
                                    get_value(value, key)
                                values[timestamp] = value
            if values:
                m = constants.metric_struct(name=key, labels=labels,
                                            values=values)
                fs_metrics.append(m)
        return fs_metrics
