# Copyright 2022 The SODA Authors.
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
import sys
from unittest import TestCase, mock

import six
from oslo_log import log

sys.modules['delfin.cryptor'] = mock.Mock()
from delfin import context
from delfin.drivers.pure.flasharray.rest_handler import RestHandler
from delfin.drivers.pure.flasharray.pure_flasharray import PureFlashArrayDriver
LOG = log.getLogger(__name__)

ACCESS_INFO = {
    "rest": {
        "host": "10.0.0.1",
        "port": 8443,
        "username": "user",
        "password": "pass"
    }
}

volumes_info = [
    {
        "total": 116272464547,
        "name": "oracl_ail",
        "system": "",
        "snapshots": 0,
        "volumes": 116272464547,
        "data_reduction": 1.82656654775252,
        "size": 2156324555567,
        "shared_space": "",
        "thin_provisioning": 0.9225557589632,
        "total_reduction": 18.92245232244555
    },
    {
        "total": 0,
        "name": "wxt1",
        "system": "",
        "snapshots": 0,
        "volumes": 0,
        "data_reduction": 1,
        "size": 1073741824,
        "shared_space": "",
        "thin_provisioning": 1,
        "total_reduction": 1
    }
]

pool_info = [
    {
        "name": "lktest",
        "volumes": [
            "oracl_ail",
            "wxt1",
            "lktest/lk301",
            "lktest/lk401",
            "lktest/lk501",
        ]
    },
    {
        "name": "ethanTestVG",
        "volumes": [

        ]
    }
]
volume_info = {
    "created": "2016-05-02T20:36:20Z",
    "name": "oracl_ail",
    "serial": "Fedd3455666y",
    "size": 1073740124,
    "source": ""
}
volume_info_two = {
    "created": "2016-05-02T20:36:20Z",
    "name": "wxt1",
    "serial": "Fedd3475666y",
    "size": 1073740124,
    "source": ""
}
storage_info = [
    {
        "parity": "0.996586544522471235",
        "provisioned": "20869257625600",
        "hostname": "FA-m20",
        "system": 0,
        "snapshots": 0,
        "volumes": 227546215656,
        "data_reduction": 1,
        "capacity": 122276719419392,
        "total": 324829845504,
        "shared_space": 97544451659,
        "thin_provisioning": 0.9526445631455244,
        "total_reduction": 64.152236458789225
    }
]
storage_id_info = {
    "array_name": "pure01",
    "id": "dlmkk15xcfdf4v5",
    "revision": "2016-20-29mfmkkk",
    "version": "4.6.7"
}
alerts_info = [
    {
        "category": "array",
        "code": 42,
        "actual": "",
        "opened": "2018-05-12T10:55:21Z",
        "component_type": "hardware",
        "event": "failure",
        "current_severity": "warning",
        "details": "",
        "expected": "",
        "id": 135,
        "component_name": "ct1.eth0"
    },
    {
        "category": "array",
        "code": 13,
        "actual": "",
        "opened": "2018-05-12T10:55:21Z",
        "component_type": "process",
        "event": "server unreachable",
        "current_severity": "warning",
        "details": "",
        "expected": "",
        "id": 10088786,
        "component_name": "ct1.ntpd"
    }
]
parse_alert_info = {
    '1.3.6.1.2.1.1.3.0': '30007589',
    '1.3.6.1.4.1.40482.3.7': '2',
    '1.3.6.1.4.1.40482.3.6': 'server error',
    '1.3.6.1.4.1.40482.3.3': 'cto',
    '1.3.6.1.4.1.40482.3.5': 'cto.server error'
}
controllers_info = [
    {
        "status": "ready",
        "name": "CT0",
        "version": "5.3.0",
        "mode": "primary",
        "model": "FA-m20r2",
        "type": "array_controller"
    },
    {
        "status": "ready",
        "name": "CT1",
        "version": "5.3.0",
        "mode": "secondary",
        "model": "FA-m20r2",
        "type": "array_controller"
    }
]
hardware_info = [
    {
        "details": "",
        "identify": "off",
        "index": 0,
        "name": "CTO.FC1",
        "slot": "",
        "speed": 0,
        "status": "ok",
        "temperature": ""
    },
    {
        "details": "",
        "identify": "",
        "index": 0,
        "name": "CTO.ETH15",
        "slot": 0,
        "speed": 1000000,
        "status": "ok",
        "temperature": ""
    }
]
drive_info = [
    {
        "status": "healthy",
        "protocol": "SAS",
        "name": "CH0.BAY1",
        "last_evac_completed": "1970-01-01T00:00:00Z",
        "details": "",
        "capacity": 1027895542547,
        "type": "SSD",
        "last_failure": "1970-01-01T00:00:00Z"
    },
    {
        "status": "healthy",
        "protocol": "SAS",
        "name": "CH0.BAY2",
        "last_evac_completed": "1970-01-01T00:00:00Z",
        "details": "",
        "capacity": 1027895542547,
        "type": "SSD",
        "last_failure": "1970-01-01T00:00:00Z"
    },
    {
        "status": "healthy",
        "protocol": "SAS",
        "name": "CH0.BAY3",
        "last_evac_completed": "1970-01-01T00:00:00Z",
        "details": "",
        "capacity": 1027895542547,
        "type": "SSD",
        "last_failure": "1970-01-01T00:00:00Z"
    }
]
port_info = [
    {
        "name": "CTO.FC1",
        "failover": "",
        "iqn": "iqn.2016-11-01.com.pure",
        "portal": "100.12.253.23:4563",
        "wwn": "43ddff45ggg4rty",
        "nqn": ""
    },
    {
        "name": "CTO.ETH15",
        "failover": "",
        "iqn": "iqn.2016-11-01.com.pure",
        "portal": "100.12.253.23:4563",
        "wwn": None,
        "nqn": None
    }
]
port_network_info = [
    {
        "name": "CTO.FC1",
        "address": "45233662jksndj",
        "speed": 12000,
        "netmask": "100.12.253.23:4563",
        "wwn": "43ddff45ggg4rty",
        "nqn": None,
        "services": [
            "management"
        ]
    },
    {
        "name": "CTO.ETH15",
        "address": "45233662jksndj",
        "speed": 13000,
        "netmask": "100.12.253.23:4563",
        "wwn": None,
        "nqn": None,
        "services": [
            "management"
        ]
    }
]
pools_info = [
    {
        "total": "",
        "name": "lktest",
        "snapshots": "",
        "volumes": 0,
        "data_reduction": 1,
        "size": 5632155322,
        "thin_provisioning": 1,
        "total_reduction": 1
    },
    {
        "total": "",
        "name": "ethanTestVG",
        "snapshots": "",
        "volumes": 0,
        "data_reduction": 1,
        "size": 5632155322,
        "thin_provisioning": 1,
        "total_reduction": 1
    }
]
reset_connection_info = {
    "username": "username",
    "status": 200
}


def create_driver():
    RestHandler.login = mock.Mock(
        return_value={None})
    return PureFlashArrayDriver(**ACCESS_INFO)


class test_PureFlashArrayDriver(TestCase):
    driver = create_driver()

    def test_init(self):
        RestHandler.login = mock.Mock(
            return_value={""})
        PureFlashArrayDriver(**ACCESS_INFO)

    def test_list_volumes(self):
        RestHandler.get_volumes = mock.Mock(
            side_effect=[volumes_info])
        volume = self.driver.list_volumes(context)
        self.assertEqual(volume[0]['native_volume_id'],
                         pool_info[0].get('volumes')[0])

    def test_get_storage(self):
        RestHandler.rest_call = mock.Mock(
            side_effect=[storage_info, hardware_info, drive_info,
                         storage_id_info, controllers_info])
        storage_object = self.driver.get_storage(context)
        self.assertEqual(storage_object.get('name'),
                         storage_id_info.get('array_name'))

    def test_list_alerts(self):
        RestHandler.rest_call = mock.Mock(
            side_effect=[alerts_info])
        list_alerts = self.driver.list_alerts(context)
        self.assertEqual(list_alerts[0].get('alert_id'),
                         alerts_info[0].get('id'))

    def test_parse_alert(self):
        parse_alert = self.driver.parse_alert(context, parse_alert_info)
        self.assertEqual(parse_alert.get('alert_id'),
                         parse_alert_info.get('1.3.6.1.2.1.1.3.0'))

    def test_list_controllers(self):
        RestHandler.rest_call = mock.Mock(
            side_effect=[controllers_info, hardware_info])
        list_controllers = self.driver.list_controllers(context)
        self.assertEqual(list_controllers[0].get('name'),
                         controllers_info[0].get('name'))

    def test_list_disks(self):
        RestHandler.rest_call = mock.Mock(
            side_effect=[hardware_info, drive_info])
        list_disks = self.driver.list_disks(context)
        self.assertEqual(list_disks[0].get('name'),
                         drive_info[0].get('name'))

    def test_list_ports(self):
        RestHandler.rest_call = mock.Mock(
            side_effect=[port_network_info, port_info, hardware_info])
        list_ports = self.driver.list_ports(context)
        self.assertEqual(list_ports[0].get('name'),
                         hardware_info[0].get('name'))

    def test_list_storage_pools(self):
        list_storage_pools = self.driver.list_storage_pools(context)
        self.assertEqual(list_storage_pools, [])

    def test_reset_connection(self):
        RestHandler.logout = mock.Mock(side_effect=None)
        RestHandler.login = mock.Mock(side_effect=None)
        username = None
        try:
            self.driver.reset_connection(context)
        except Exception as e:
            LOG.error("test_reset_connection error: %s", six.text_type(e))
            username = reset_connection_info.get('username')
        self.assertEqual(username, None)
