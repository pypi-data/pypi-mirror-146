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
from delfin import exception
from delfin.common import constants

SOCKET_TIMEOUT = 30
LOGIN_SOCKET_TIMEOUT = 10
CER_ERR = 'Unable to validate the identity of the server'
CALLER_ERR = 'Caller not privileged'
SECURITY_ERR = 'Security file not found'
TRYING_CONNECT_ERR = 'error occurred while trying to connect'
CONNECTION_ERR = 'connection refused'
INVALID_ERR = 'invalid username, password and/or scope'
NOT_SUPPORTED_ERR = 'CLI commands are not supported by the target storage' \
                    ' system'
EXCEPTION_MAP = {CER_ERR: exception.SSLCertificateFailed,
                 CALLER_ERR: exception.InvalidUsernameOrPassword,
                 SECURITY_ERR: exception.InvalidUsernameOrPassword,
                 TRYING_CONNECT_ERR: exception.InvalidIpOrPort,
                 CONNECTION_ERR: exception.InvalidIpOrPort,
                 INVALID_ERR: exception.InvalidUsernameOrPassword,
                 NOT_SUPPORTED_ERR: exception.StorageBackendException}
CER_STORE = '2'
CER_REJECT = '3'
DISK_ID_KEY = 'Bus 0 Enclosure 0  Disk'
LUN_ID_KEY = 'LOGICAL UNIT NUMBER'
LUN_NAME_KEY = 'Name                        '
CER_SEPARATE_KEY = '-----------------------------'
TIME_PATTERN = '%m/%d/%Y %H:%M:%S'
DATE_PATTERN = '%m/%d/%Y'
ONE_DAY_SCE = 24 * 60 * 60
LOG_FILTER_PATTERN = '\\(7[0-7]([a-f]|[0-9]){2}\\)'
NAVISECCLI_API = 'naviseccli -User %(username)s -password %(password)s' \
                 ' -scope 0 -t %(timeout)d -h %(host)s'
CER_ADD_API = 'naviseccli security -certificate -add -file'
CER_LIST_API = 'naviseccli security -certificate -list'
CER_REMOVE_API = 'naviseccli security -certificate -remove'
GET_AGENT_API = 'getagent'
GET_DOMAIN_API = 'domain -list'
GET_STORAGEPOOL_API = 'storagepool -list'
GET_RAIDGROUP_API = 'getrg'
GET_DISK_API = 'getdisk'
GET_LUN_API = 'lun -list'
GET_GETALLLUN_API = 'getall -lun'
GET_SP_API = 'getsp'
GET_PORT_API = 'port -list -sp -all'
GET_BUS_PORT_API = 'backendbus -get -all'
GET_BUS_PORT_STATE_API = 'ioportconfig -list -iomodule basemodule' \
                         ' -portstate -pportid'
GET_ISCSI_PORT_API = 'connection -getport'
GET_IO_PORT_CONFIG_API = 'ioportconfig -list -all'
GET_RESUME_API = 'getresume -all'
GET_LOG_API = 'getlog -date %(begin_time)s %(end_time)s'
EMCVNX_VENDOR = 'DELL EMC'
RAID_GROUP_ID_PREFIX = 'raid_group_'
STATUS_MAP = {
    'Ready': constants.StoragePoolStatus.NORMAL,
    'Offline': constants.StoragePoolStatus.OFFLINE,
    'Valid_luns': constants.StoragePoolStatus.NORMAL,
    'Busy': constants.StoragePoolStatus.ABNORMAL,
    'Halted': constants.StoragePoolStatus.ABNORMAL,
    'Defragmenting': constants.StoragePoolStatus.NORMAL,
    'Expanding': constants.StoragePoolStatus.NORMAL,
    'Explicit Remove': constants.StoragePoolStatus.OFFLINE,
    'Invalid': constants.StoragePoolStatus.OFFLINE,
    'Bound': constants.StoragePoolStatus.NORMAL
}
VOL_TYPE_MAP = {'no': constants.VolumeType.THICK,
                'yes': constants.VolumeType.THIN}
VOL_COMPRESSED_MAP = {'no': False,
                      'yes': True}
DEFAULT_QUERY_LOG_DAYS = 9
SECS_OF_TEN_DAYS = DEFAULT_QUERY_LOG_DAYS * ONE_DAY_SCE
OID_SEVERITY = '1.3.6.1.6.3.1.1.4.1.0'
OID_MESSAGECODE = '1.3.6.1.4.1.1981.1.4.5'
OID_DETAILS = '1.3.6.1.4.1.1981.1.4.6'
SEVERITY_MAP = {"76": constants.Severity.CRITICAL,
                "75": constants.Severity.MAJOR,
                "74": constants.Severity.MINOR,
                "73": constants.Severity.WARNING,
                "72": constants.Severity.WARNING,
                "77": constants.Severity.FATAL,
                "71": constants.Severity.INFORMATIONAL,
                "70": constants.Severity.INFORMATIONAL}
TRAP_LEVEL_MAP = {'1.3.6.1.4.1.1981.0.6': constants.Severity.CRITICAL,
                  '1.3.6.1.4.1.1981.0.5': constants.Severity.MINOR,
                  '1.3.6.1.4.1.1981.0.4': constants.Severity.WARNING,
                  '1.3.6.1.4.1.1981.0.3': constants.Severity.INFORMATIONAL,
                  '1.3.6.1.4.1.1981.0.2': constants.Severity.INFORMATIONAL
                  }
DISK_STATUS_MAP = {
    'BINDING': constants.DiskStatus.ABNORMAL,
    'ENABLED': constants.DiskStatus.NORMAL,
    'EMPTY': constants.DiskStatus.ABNORMAL,
    'EXPANDING': constants.DiskStatus.ABNORMAL,
    'FORMATTING': constants.DiskStatus.ABNORMAL,
    'OFF': constants.DiskStatus.ABNORMAL,
    'POWERING UP': constants.DiskStatus.ABNORMAL,
    'REBUILDING': constants.DiskStatus.ABNORMAL,
    'REMOVED': constants.DiskStatus.ABNORMAL,
    'UNASSIGNED': constants.DiskStatus.ABNORMAL,
    'UNBOUND': constants.DiskStatus.NORMAL,
    'UNFORMATTED': constants.DiskStatus.ABNORMAL,
    'UNSUPPORTED': constants.DiskStatus.ABNORMAL
}
DISK_PHYSICAL_TYPE_MAP = {
    'SATA': constants.DiskPhysicalType.SATA,
    'SAS': constants.DiskPhysicalType.SAS,
    'SSD': constants.DiskPhysicalType.SSD,
    'NL-SAS': constants.DiskPhysicalType.NL_SAS,
    'NL-SSD': constants.DiskPhysicalType.NL_SSD,
    'FLASH': constants.DiskPhysicalType.FLASH,
    'SAS FLASH VP': constants.DiskPhysicalType.SAS_FLASH_VP,
    'FIBRE CHANNEL': constants.DiskPhysicalType.FC,
    'ATA': constants.DiskPhysicalType.ATA
}
SPPORT_KEY = "Information about each SPPORT:"
PORT_CONNECTION_STATUS_MAP = {
    'UP': constants.PortConnectionStatus.CONNECTED,
    'DOWN': constants.PortConnectionStatus.DISCONNECTED
}
PORT_HEALTH_STATUS_MAP = {
    'ONLINE': constants.PortHealthStatus.NORMAL,
    'DISABLED': constants.PortHealthStatus.ABNORMAL,
    'ENABLED': constants.PortHealthStatus.NORMAL,
    'MISSING': constants.PortHealthStatus.ABNORMAL
}
PORT_TYPE_MAP = {
    'FIBRE': constants.PortType.FC,
    'FCOE': constants.PortType.FCOE,
    'ISCSI': constants.PortType.ISCSI,
    'SAS': constants.PortType.SAS,
    'UNKNOWN': constants.PortType.OTHER
}
