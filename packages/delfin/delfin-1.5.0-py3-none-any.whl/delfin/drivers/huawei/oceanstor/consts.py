# Copyright 2020 The SODA Authors.
# Copyright (c) 2016 Huawei Technologies Co., Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from delfin.common import constants

STATUS_HEALTH = '1'
STATUS_ACTIVE = '43'
STATUS_RUNNING = '10'
STATUS_VOLUME_READY = '27'
STATUS_LUNCOPY_READY = '40'
STATUS_QOS_ACTIVE = '2'
QOS_INACTIVATED = '45'
LUN_TYPE = '11'
SNAPSHOT_TYPE = '27'
STATUS_POOL_ONLINE = '27'
STATUS_STORAGE_NORMAL = '1'
STATUS_CTRLR_OFFLINE = '28'
STATUS_CTRLR_UNKNOWN = '0'

PORT_TYPE_FC = '212'
PORT_TYPE_ETH = '213'
PORT_TYPE_SAS = '214'
PORT_TYPE_FCOE = '252'
PORT_TYPE_PCIE = '233'
PORT_TYPE_BOND = '235'

PORT_LOGICTYPE_HOST = '0'
PORT_HEALTH_UNKNOWN = '0'
PORT_HEALTH_NORMAL = '1'
PORT_HEALTH_FAULTY = '2'
PORT_HEALTH_ABOUTFAIL = '3'
PORT_HEALTH_PARTIALLYDAMAGED = '4'
PORT_HEALTH_INCONSISTENT = '9'

PORT_RUNNINGSTS_UNKNOWN = '0'
PORT_RUNNINGSTS_NORMAL = '1'
PORT_RUNNINGSTS_RUNNING = '2'
PORT_RUNNINGSTS_LINKUP = '10'
PORT_RUNNINGSTS_LINKDOWN = '11'
PORT_RUNNINGSTS_TOBERECOVERED = '33'

PORT_LOGICTYPE_EXPANSION = '1'
PORT_LOGICTYPE_MANAGEMENT = '2'
PORT_LOGICTYPE_INTERNAL = '3'
PORT_LOGICTYPE_MAINTENANCE = '4'
PORT_LOGICTYPE_SERVICE = '5'
PORT_LOGICTYPE_MAINTENANCE2 = '6'
PORT_LOGICTYPE_INTERCONNECT = '11'

PortTypeMap = {
    PORT_TYPE_FC: constants.PortType.FC,
    PORT_TYPE_FCOE: constants.PortType.FCOE,
    PORT_TYPE_ETH: constants.PortType.ETH,
    PORT_TYPE_PCIE: constants.PortType.OTHER,
    PORT_TYPE_SAS: constants.PortType.SAS,
    PORT_TYPE_BOND: constants.PortType.OTHER,
}

PortLogicTypeMap = {
    PORT_LOGICTYPE_HOST:
        constants.PortLogicalType.SERVICE,
    PORT_LOGICTYPE_EXPANSION:
        constants.PortLogicalType.OTHER,
    PORT_LOGICTYPE_MANAGEMENT:
        constants.PortLogicalType.MANAGEMENT,
    PORT_LOGICTYPE_INTERNAL:
        constants.PortLogicalType.INTERNAL,
    PORT_LOGICTYPE_MAINTENANCE:
        constants.PortLogicalType.MAINTENANCE,
    PORT_LOGICTYPE_SERVICE:
        constants.PortLogicalType.SERVICE,
    PORT_LOGICTYPE_MAINTENANCE2:
        constants.PortLogicalType.MAINTENANCE,
    PORT_LOGICTYPE_INTERCONNECT:
        constants.PortLogicalType.INTERCONNECT,
}

DISK_STATUS_UNKNOWN = '0'
DISK_STATUS_NORMAL = '1'
DISK_STATUS_OFFLINE = '28'

DISK_TYPE_SAS = '1'
DISK_TYPE_SATA = '2'
DISK_TYPE_SSD = '3'

DISK_LOGICTYPE_FREE = '1'
DISK_LOGICTYPE_MEMBER = '2'
DISK_LOGICTYPE_HOTSPARE = '3'
DISK_LOGICTYPE_CACHE = '4'

DiskPhysicalTypeMap = {
    DISK_TYPE_SATA: constants.DiskPhysicalType.SATA,
    DISK_TYPE_SAS: constants.DiskPhysicalType.SAS,
    DISK_TYPE_SSD: constants.DiskPhysicalType.SSD,
}

DiskLogicalTypeMap = {
    DISK_LOGICTYPE_FREE:
        constants.DiskLogicalType.FREE,
    DISK_LOGICTYPE_MEMBER:
        constants.DiskLogicalType.MEMBER,
    DISK_LOGICTYPE_HOTSPARE:
        constants.DiskLogicalType.HOTSPARE,
    DISK_LOGICTYPE_CACHE:
        constants.DiskLogicalType.CACHE,
}

FS_WORM_COMPLIANCE = '1'
FS_WORM_AUDIT_LOG = '2'
FS_WORM_ENTERPRISE = '3'

FS_HEALTH_NORMAL = '1'
FS_TYPE_THICK = '0'
FS_TYPE_THIN = '1'
PARENT_TYPE_POOL = 216

QUOTA_NOT_ENABLED = 'INVALID_VALUE64'
QUOTA_TYPE_TREE = '1'
QUOTA_TYPE_USER = '2'
QUOTA_TYPE_GROUP = '3'

SECURITY_STYLE_MIXED = '0'
SECURITY_STYLE_NATIVE = '1'
SECURITY_STYLE_NTFS = '2'
SECURITY_STYLE_UNIX = '3'

PARENT_OBJECT_TYPE_FS = 40
SHARE_NFS = '16401'

ERROR_CONNECT_TO_SERVER = -403
ERROR_UNAUTHORIZED_TO_SERVER = -401

SOCKET_TIMEOUT = 52
LOGIN_SOCKET_TIMEOUT = 4

ERROR_VOLUME_NOT_EXIST = 1077939726
RELOGIN_ERROR_PASS = [ERROR_VOLUME_NOT_EXIST]
PWD_EXPIRED = 3
PWD_RESET = 4

BLOCK_STORAGE_POOL_TYPE = '1'
FILE_SYSTEM_POOL_TYPE = '2'

SECTORS_SIZE = 512
QUERY_PAGE_SIZE = 100

THICK_LUNTYPE = '0'
THIN_LUNTYPE = '1'

HOST_OS = [
    constants.HostOSTypes.LINUX,
    constants.HostOSTypes.WINDOWS,
    constants.HostOSTypes.SOLARIS,
    constants.HostOSTypes.HP_UX,
    constants.HostOSTypes.AIX,
    constants.HostOSTypes.XEN_SERVER,
    constants.HostOSTypes.VMWARE_ESX,
    constants.HostOSTypes.LINUX_VIS,
    constants.HostOSTypes.WINDOWS_SERVER_2012,
    constants.HostOSTypes.ORACLE_VM,
    constants.HostOSTypes.OPEN_VMS,
]

HOST_RUNNINGSTATUS_NORMAL = '1'
INITIATOR_RUNNINGSTATUS_UNKNOWN = '0'
INITIATOR_RUNNINGSTATUS_ONLINE = '27'
INITIATOR_RUNNINGSTATUS_OFFLINE = '28'
ISCSI_INITIATOR_TYPE = 222
FC_INITIATOR_TYPE = 223
IB_INITIATOR_TYPE = 16499
ISCSI_INITIATOR_DESCRIPTION = 'iSCSI Initiator'
FC_INITIATOR_DESCRIPTION = 'FC Initiator'
IB_INITIATOR_DESCRIPTION = 'IB Initiator'
UNKNOWN_INITIATOR_DESCRIPTION = 'Unknown Initiator'

OCEANSTOR_METRICS = {
    'iops': '22',
    'readIops': '25',
    'writeIops': '28',
    'throughput': '21',
    'readThroughput': '23',
    'writeThroughput': '26',
    'responseTime': '370',
    'ioSize': '228',
    'readIoSize': '24',
    'writeIoSize': '27',
    'cacheHitRatio': '303',
    'readCacheHitRatio': '93',
    'writeCacheHitRatio': '95',
}

CONVERT_TO_MILLI_SECOND_LIST = [
    'responseTime'
]

IOPS_DESCRIPTION = {
    "unit": "IOPS",
    "description": "Input/output operations per second"
}
READ_IOPS_DESCRIPTION = {
    "unit": "IOPS",
    "description": "Read input/output operations per second"
}
WRITE_IOPS_DESCRIPTION = {
    "unit": "IOPS",
    "description": "Write input/output operations per second"
}
THROUGHPUT_DESCRIPTION = {
    "unit": "MB/s",
    "description": "Represents how much data is "
                   "successfully transferred in MB/s"
}
READ_THROUGHPUT_DESCRIPTION = {
    "unit": "MB/s",
    "description": "Represents how much data read is "
                   "successfully transferred in MB/s"
}
WRITE_THROUGHPUT_DESCRIPTION = {
    "unit": "MB/s",
    "description": "Represents how much data write is "
                   "successfully transferred in MB/s"
}
RESPONSE_TIME_DESCRIPTION = {
    "unit": "ms",
    "description": "Average time taken for an IO "
                   "operation in ms"
}
CACHE_HIT_RATIO_DESCRIPTION = {
    "unit": "%",
    "description": "Percentage of io that are cache hits"
}
READ_CACHE_HIT_RATIO_DESCRIPTION = {
    "unit": "%",
    "description": "Percentage of read ops that are cache hits"
}
WRITE_CACHE_HIT_RATIO_DESCRIPTION = {
    "unit": "%",
    "description": "Percentage of write ops that are cache hits"
}
IO_SIZE_DESCRIPTION = {
    "unit": "KB",
    "description": "The average size of IO requests in KB"
}
READ_IO_SIZE_DESCRIPTION = {
    "unit": "KB",
    "description": "The average size of read IO requests in KB"
}
WRITE_IO_SIZE_DESCRIPTION = {
    "unit": "KB",
    "description": "The average size of write IO requests in KB"
}
CPU_USAGE_DESCRIPTION = {
    "unit": "%",
    "description": "Percentage of CPU usage"
}
MEMORY_USAGE_DESCRIPTION = {
    "unit": "%",
    "description": "Percentage of DISK memory usage in percentage"
}
SERVICE_TIME = {
    "unit": 'ms',
    "description": "Service time of the resource in ms"
}
POOL_CAP = {
    "iops": IOPS_DESCRIPTION,
    "readIops": READ_IOPS_DESCRIPTION,
    "writeIops": WRITE_IOPS_DESCRIPTION,
    "throughput": THROUGHPUT_DESCRIPTION,
    "readThroughput": READ_THROUGHPUT_DESCRIPTION,
    "writeThroughput": WRITE_THROUGHPUT_DESCRIPTION,
    "responseTime": RESPONSE_TIME_DESCRIPTION,
}
VOLUME_CAP = {
    "iops": IOPS_DESCRIPTION,
    "readIops": READ_IOPS_DESCRIPTION,
    "writeIops": WRITE_IOPS_DESCRIPTION,
    "throughput": THROUGHPUT_DESCRIPTION,
    "readThroughput": READ_THROUGHPUT_DESCRIPTION,
    "writeThroughput": WRITE_THROUGHPUT_DESCRIPTION,
    "responseTime": RESPONSE_TIME_DESCRIPTION,
    "cacheHitRatio": CACHE_HIT_RATIO_DESCRIPTION,
    "readCacheHitRatio": READ_CACHE_HIT_RATIO_DESCRIPTION,
    "writeCacheHitRatio": WRITE_CACHE_HIT_RATIO_DESCRIPTION,
    "ioSize": IO_SIZE_DESCRIPTION,
    "readIoSize": READ_IO_SIZE_DESCRIPTION,
    "writeIoSize": WRITE_IO_SIZE_DESCRIPTION,
}
CONTROLLER_CAP = {
    "iops": IOPS_DESCRIPTION,
    "readIops": READ_IOPS_DESCRIPTION,
    "writeIops": WRITE_IOPS_DESCRIPTION,
    "throughput": THROUGHPUT_DESCRIPTION,
    "readThroughput": READ_THROUGHPUT_DESCRIPTION,
    "writeThroughput": WRITE_THROUGHPUT_DESCRIPTION,
    "responseTime": RESPONSE_TIME_DESCRIPTION,
}
PORT_CAP = {
    "iops": IOPS_DESCRIPTION,
    "readIops": READ_IOPS_DESCRIPTION,
    "writeIops": WRITE_IOPS_DESCRIPTION,
    "throughput": THROUGHPUT_DESCRIPTION,
    "readThroughput": READ_THROUGHPUT_DESCRIPTION,
    "writeThroughput": WRITE_THROUGHPUT_DESCRIPTION,
    "responseTime": RESPONSE_TIME_DESCRIPTION,
}
DISK_CAP = {
    "iops": IOPS_DESCRIPTION,
    "readIops": READ_IOPS_DESCRIPTION,
    "writeIops": WRITE_IOPS_DESCRIPTION,
    "throughput": THROUGHPUT_DESCRIPTION,
    "readThroughput": READ_THROUGHPUT_DESCRIPTION,
    "writeThroughput": WRITE_THROUGHPUT_DESCRIPTION,
    "responseTime": RESPONSE_TIME_DESCRIPTION,
}
