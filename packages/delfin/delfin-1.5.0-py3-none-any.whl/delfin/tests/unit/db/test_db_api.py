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

from unittest import mock

from delfin import context, exception
from delfin import test
from delfin.db import api as db_api
from delfin.db.sqlalchemy import api, models
from delfin.tests.unit import fake_data, utils

ctxt = context.get_admin_context()


class TestIMDBAPIStoragePool(test.TestCase):
    @mock.patch('sqlalchemy.create_engine', mock.Mock())
    def test_register_db(self):
        db_api.register_db()

    def test_get_session(self):
        api.get_session()

    def test_get_engine(self):
        api.get_engine()

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_basic_storage_pool_create(self, mock_session):
        storage_pool_model_lst = fake_data.fake_storage_pool_create()
        expected = fake_data.fake_expected_storage_pool_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_pools_create(ctxt, storage_pool_model_lst)
        utils.validate_db_schema_model(got[0], models.StoragePool)
        utils.validate_db_schema_model(expected[0], models.StoragePool)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_unknown_attribute_storage_pool_model_create(self, mock_session):
        storage_pool_model_lst = fake_data.fake_storage_pool_create()
        expected = fake_data.fake_expected_storage_pool_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_pools_create(ctxt, storage_pool_model_lst)
        self.assertRaisesRegex(AssertionError, "",
                               utils.validate_db_schema_model,
                               got[1], models.StoragePool)


class TestSIMDBAPI(test.TestCase):

    @mock.patch('sqlalchemy.create_engine', mock.Mock())
    def test_register_db(self):
        db_api.register_db()

    def test_get_session(self):
        api.get_session()

    def test_get_engine(self):
        api.get_engine()

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_get(self, mock_session):
        fake_storage = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_get(ctxt,
                                    'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_update(self, mock_session):
        fake_storage = models.Storage()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_update(ctxt,
                                       'c5c91c98-91aa-40e6-85ac-37a1d3b32bda',
                                       fake_storage)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_delete(self, mock_session):
        fake_storage = models.Storage()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_delete(ctxt,
                                       'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_create(self, mock_session):
        fake_storage = models.Storage()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_create(ctxt, fake_storage)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_get_all(self, mock_session):
        fake_storage = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_get_all(ctxt)
        assert len(result) == 0

        mock_session.return_value.__enter__.return_value.query = fake_storage
        result = db_api.storage_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

        result = db_api.storage_get_all(ctxt, limit=1)
        assert len(result) == 0

        result = db_api.storage_get_all(ctxt, offset=3)
        assert len(result) == 0

        result = db_api.storage_get_all(ctxt, sort_dirs=['desc'],
                                        sort_keys=['name'])
        assert len(result) == 0

        self.assertRaises(exception.InvalidInput, api.storage_get_all,
                          ctxt, sort_dirs=['desc', 'asc'],
                          sort_keys=['name'])

        self.assertRaises(exception.InvalidInput, api.storage_get_all,
                          ctxt, sort_dirs=['desc_err'],
                          sort_keys=['name'])

        result = db_api.storage_get_all(ctxt, sort_dirs=['desc'],
                                        sort_keys=['name', 'id'])
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pool_get(self, mock_session):
        fake_storage_pool = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage_pool
        result = db_api.storage_pool_get(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pool_get_all(self, mock_session):
        fake_storage_pool = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage_pool
        result = api.storage_pool_get_all(context)
        assert len(result) == 0

        result = db_api.storage_pool_get_all(context,
                                             filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pools_update(self, mock_session):
        storage_pools = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_pools
        result = db_api.storage_pools_update(context, storage_pools)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pool_update(self, mock_session):
        values = {'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = values
        result = db_api.storage_pool_update(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', values)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pools_delete(self, mock_session):
        fake_storage_pools = [models.StoragePool().id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage_pools
        result = db_api.storage_pools_delete(context, fake_storage_pools)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pools_create(self, mock_session):
        fake_storage_pools = [models.StoragePool()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage_pools
        result = db_api.storage_pools_create(context, fake_storage_pools)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_pool_create(self, mock_session):
        fake_storage_pool = models.StoragePool()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage_pool
        result = db_api.storage_pool_create(context, fake_storage_pool)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_get(self, mock_session):
        fake_volume = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volume_get(ctxt,
                                   'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volumes_update(self, mock_session):
        volumes = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = volumes
        result = db_api.volumes_update(ctxt, volumes)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_update(self, mock_session):
        volumes = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = volumes
        result = db_api.volume_update(ctxt,
                                      'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                      volumes)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volumes_delete(self, mock_session):
        fake_volume = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volumes_delete(ctxt, fake_volume)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volumes_create(self, mock_session):
        fake_volume = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volumes_create(ctxt, fake_volume)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_create(self, mock_session):
        fake_volume = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volume_create(ctxt, fake_volume)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_get_all(self, mock_session):
        fake_volume = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volume_get_all(ctxt)
        assert len(result) == 0

        result = db_api.volume_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controller_get(self, mock_session):
        fake_controller = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_controller
        result = db_api.controller_get(ctxt,
                                       'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controllers_update(self, mock_session):
        controllers = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = controllers
        result = db_api.controllers_update(ctxt, controllers)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controller_update(self, mock_session):
        controllers = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = controllers
        result = db_api.controller_update(
            ctxt, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', controllers)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controllers_delete(self, mock_session):
        fake_controller = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_controller
        result = db_api.controllers_delete(ctxt, fake_controller)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controllers_create(self, mock_session):
        fake_controller = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_controller
        result = db_api.controllers_create(ctxt, fake_controller)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controller_create(self, mock_session):
        fake_controller = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_controller
        result = db_api.controller_create(ctxt, fake_controller)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_controller_get_all(self, mock_session):
        fake_controller = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_controller
        result = db_api.controller_get_all(ctxt)
        assert len(result) == 0

        result = db_api.controller_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_get(self, mock_session):
        fake_port = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_port
        result = db_api.port_get(ctxt,
                                 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_ports_update(self, mock_session):
        ports = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = ports
        result = db_api.ports_update(ctxt, ports)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_update(self, mock_session):
        ports = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = ports
        result = db_api.port_update(ctxt,
                                    'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                    ports)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_ports_delete(self, mock_session):
        fake_port = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_port
        result = db_api.ports_delete(ctxt, fake_port)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_ports_create(self, mock_session):
        fake_port = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_port
        result = db_api.ports_create(ctxt, fake_port)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_create(self, mock_session):
        fake_port = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_port
        result = db_api.port_create(ctxt, fake_port)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_get_all(self, mock_session):
        fake_port = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_port
        result = db_api.port_get_all(ctxt)
        assert len(result) == 0

        result = db_api.port_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disk_get(self, mock_session):
        fake_disk = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_disk
        result = db_api.disk_get(ctxt,
                                 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disks_update(self, mock_session):
        disks = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = disks
        result = db_api.disks_update(ctxt, disks)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disk_update(self, mock_session):
        disks = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = disks
        result = db_api.disk_update(ctxt,
                                    'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                    disks)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disks_delete(self, mock_session):
        fake_disk = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_disk
        result = db_api.disks_delete(ctxt, fake_disk)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disks_create(self, mock_session):
        fake_disk = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_disk
        result = db_api.disks_create(ctxt, fake_disk)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disk_create(self, mock_session):
        fake_disk = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_disk
        result = db_api.disk_create(ctxt, fake_disk)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_disk_get_all(self, mock_session):
        fake_disk = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_disk
        result = db_api.disk_get_all(ctxt)
        assert len(result) == 0

        result = db_api.disk_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystem_get(self, mock_session):
        fake_filesystem = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_filesystem
        result = db_api.filesystem_get(ctxt,
                                       'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystems_update(self, mock_session):
        filesystems = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = filesystems
        result = db_api.filesystems_update(ctxt, filesystems)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystem_update(self, mock_session):
        filesystems = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = filesystems
        result = db_api.filesystem_update(
            ctxt, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', filesystems)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystems_delete(self, mock_session):
        fake_filesystem = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_filesystem
        result = db_api.filesystems_delete(ctxt, fake_filesystem)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystems_create(self, mock_session):
        fake_filesystem = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_filesystem
        result = db_api.filesystems_create(ctxt, fake_filesystem)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystem_create(self, mock_session):
        fake_filesystem = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_filesystem
        result = db_api.filesystem_create(ctxt, fake_filesystem)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_filesystem_get_all(self, mock_session):
        fake_filesystem = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_filesystem
        result = db_api.filesystem_get_all(ctxt)
        assert len(result) == 0

        result = db_api.filesystem_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtree_get(self, mock_session):
        fake_qtree = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_qtree
        result = db_api.qtree_get(ctxt,
                                  'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtrees_update(self, mock_session):
        qtrees = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = qtrees
        result = db_api.qtrees_update(ctxt, qtrees)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtree_update(self, mock_session):
        qtrees = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = qtrees
        result = db_api.qtree_update(ctxt,
                                     'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                     qtrees)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtrees_delete(self, mock_session):
        fake_qtree = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_qtree
        result = db_api.qtrees_delete(ctxt, fake_qtree)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtrees_create(self, mock_session):
        fake_qtree = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_qtree
        result = db_api.qtrees_create(ctxt, fake_qtree)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtree_create(self, mock_session):
        fake_qtree = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_qtree
        result = db_api.qtree_create(ctxt, fake_qtree)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_qtree_get_all(self, mock_session):
        fake_qtree = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_qtree
        result = db_api.qtree_get_all(ctxt)
        assert len(result) == 0

        result = db_api.qtree_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quota_get(self, mock_session):
        fake_quota = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_quota
        result = db_api.quota_get(ctxt,
                                  'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quotas_update(self, mock_session):
        quotas = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = quotas
        result = db_api.quotas_update(ctxt, quotas)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quota_update(self, mock_session):
        quotas = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = quotas
        result = db_api.quota_update(ctxt,
                                     'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                     quotas)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quotas_delete(self, mock_session):
        fake_quota = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_quota
        result = db_api.quotas_delete(ctxt, fake_quota)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quotas_create(self, mock_session):
        fake_quota = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_quota
        result = db_api.quotas_create(ctxt, fake_quota)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quota_create(self, mock_session):
        fake_quota = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_quota
        result = db_api.quota_create(ctxt, fake_quota)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_quota_get_all(self, mock_session):
        fake_quota = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_quota
        result = db_api.quota_get_all(ctxt)
        assert len(result) == 0

        result = db_api.quota_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_share_get(self, mock_session):
        fake_share = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_share
        result = db_api.share_get(ctxt,
                                  'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_shares_update(self, mock_session):
        shares = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = shares
        result = db_api.shares_update(ctxt, shares)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_share_update(self, mock_session):
        shares = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = shares
        result = db_api.share_update(ctxt,
                                     'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                     shares)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_shares_delete(self, mock_session):
        fake_share = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_share
        result = db_api.shares_delete(ctxt, fake_share)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_shares_create(self, mock_session):
        fake_share = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_share
        result = db_api.shares_create(ctxt, fake_share)
        assert len(result) == 1

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_share_create(self, mock_session):
        fake_share = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_share
        result = db_api.share_create(ctxt, fake_share)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_share_get_all(self, mock_session):
        fake_share = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_share
        result = db_api.share_get_all(ctxt)
        assert len(result) == 0

        result = db_api.share_get_all(ctxt, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_access_info_get_all(self, mock_session):
        fake_access_info = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_get_all(ctxt)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_access_info_get(self, mock_session):
        fake_access_info = models.AccessInfo()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_get(ctxt,
                                        'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_access_info_create(self, mock_session):
        fake_access_info = models.AccessInfo()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_create(ctxt, fake_access_info)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_access_info_update(self, mock_session):
        fake_access_info = models.AccessInfo()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_update(
            ctxt, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', fake_access_info)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_alert_source_get_all(self, mock_session):
        fake_alert_source = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_get_all(ctxt)
        assert len(result) == 0

        result = db_api.alert_source_get_all(ctxt,
                                             filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_alert_source_update(self, mock_session):
        fake_alert_source = models.AlertSource()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_update(
            ctxt, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', fake_alert_source)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_alert_source_delete(self, mock_session):
        fake_alert_source = models.AlertSource()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_delete(
            ctxt, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_alert_source_create(self, mock_session):
        fake_alert_source = models.AlertSource()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_create(ctxt, fake_alert_source)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_task_create(self, mock_session):
        fake_task = models.Task()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_task
        result = db_api.task_create(context, fake_task)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_task_update(self, mock_session):
        values = {'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = values
        result = db_api.task_update(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', values)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_task_get(self, mock_session):
        fake_task = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_task
        result = db_api.task_get(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_task_get_all(self, mock_session):
        fake_task = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_task
        result = api.task_get_all(context)
        assert len(result) == 0

        result = db_api.task_get_all(context,
                                     filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_task_delete(self, mock_session):
        fake_task = [models.Task().id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_task
        result = db_api.task_delete(context, fake_task)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_task_delete_by_storage(self, mock_session):
        fake_task_storage_id = [models.Task().storage_id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_task_storage_id
        result = db_api \
            .task_delete_by_storage(context, fake_task_storage_id)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_create(self, mock_session):
        fake_failed_task = models.FailedTask()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_failed_task
        result = db_api.failed_task_create(context, fake_failed_task)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_update(self, mock_session):
        values = {'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = values
        result = db_api.failed_task_update(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', values)
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_get(self, mock_session):
        fake_failed_task = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_failed_task
        result = db_api.failed_task_get(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_get_all(self, mock_session):
        fake_failed_task = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_failed_task
        result = api.failed_task_get_all(context)
        assert len(result) == 0

        result = db_api.failed_task_get_all(context,
                                            filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_delete(self, mock_session):
        fake_failed_task = [models.FailedTask().id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_failed_task
        result = db_api.task_delete(context, fake_failed_task)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_delete_by_task_id(self, mock_session):
        fake_failed_task_id \
            = [models.FailedTask().task_id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_failed_task_id
        result = db_api \
            .failed_task_delete_by_task_id(context,
                                           fake_failed_task_id)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_failed_task_delete_by_storage(self, mock_session):
        fake_failed_task_storage_id = [models.FailedTask().storage_id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_failed_task_storage_id
        result = db_api \
            .task_delete_by_storage(context, fake_failed_task_storage_id)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_basic_storage_pool_create(self, mock_session):
        storage_pool_model_lst = fake_data.fake_storage_pool_create()
        expected = fake_data.fake_expected_storage_pool_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_pools_create(ctxt, storage_pool_model_lst)
        utils.validate_db_schema_model(got[0], models.StoragePool)
        utils.validate_db_schema_model(expected[0], models.StoragePool)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_unknown_attribute_storage_pool_model_create(self, mock_session):
        storage_pool_model_lst = fake_data.fake_storage_pool_create()
        expected = fake_data.fake_expected_storage_pool_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_pools_create(ctxt, storage_pool_model_lst)
        self.assertRaisesRegex(AssertionError, "",
                               utils.validate_db_schema_model,
                               got[1], models.StoragePool)

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_initiator_create(self, mock_session):
        storage_host_initiator_model_lst \
            = fake_data.fake_storage_host_initiator_create()
        expected = fake_data.fake_expected_storage_host_initiator_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_host_initiators_create(
            ctxt, storage_host_initiator_model_lst)
        utils.validate_db_schema_model(got[0], models.StorageHostInitiator)
        utils.validate_db_schema_model(expected[0],
                                       models.StorageHostInitiator)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_initiator_update(self, mock_session):
        storage_host_initiator_model_lst \
            = fake_data.fake_storage_host_initiator_create()
        expected = fake_data.fake_expected_storage_host_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        result = db_api.storage_host_initiators_update(
            ctxt, storage_host_initiator_model_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_initiator_delete(self, mock_session):
        storage_host_initiator_model_lst \
            = fake_data.fake_storage_host_initiator_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_host_initiator_model_lst
        result = db_api.storage_host_initiators_delete(
            ctxt, storage_host_initiator_model_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_initiator_delete_by_storage(self, mock_session):
        storage_host_initiator_model_lst \
            = fake_data.fake_storage_host_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_host_initiator_model_lst
        result = db_api.storage_host_initiators_delete_by_storage(
            ctxt, storage_host_initiator_model_lst[0]['storage_id'])
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_create(self, mock_session):
        storage_host_model_lst \
            = fake_data.fake_storage_host_create()
        expected = fake_data.fake_expected_storage_host_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_hosts_create(
            ctxt, storage_host_model_lst)
        utils.validate_db_schema_model(got[0], models.StorageHost)
        utils.validate_db_schema_model(expected[0], models.StorageHost)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_update(self, mock_session):
        storage_host_model_lst \
            = fake_data.fake_storage_host_create()
        expected = fake_data.fake_expected_storage_host_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        result = db_api.storage_hosts_update(ctxt, storage_host_model_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_delete(self, mock_session):
        storage_host_model_lst \
            = fake_data.fake_storage_host_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_host_model_lst
        result = db_api.storage_hosts_delete(ctxt, storage_host_model_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_delete_by_storage(self, mock_session):
        storage_host_model_lst \
            = fake_data.fake_storage_host_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_host_model_lst
        result = db_api.storage_hosts_delete_by_storage(
            ctxt, storage_host_model_lst[0]['storage_id'])
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_groups_create(self, mock_session):
        storage_host_group_lst \
            = fake_data.fake_storage_host_group_create()
        expected = fake_data.fake_expected_storage_host_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.storage_host_groups_create(
            ctxt, storage_host_group_lst)
        utils.validate_db_schema_model(got[0], models.StorageHostGroup)
        utils.validate_db_schema_model(expected[0], models.StorageHostGroup)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_group_update(self, mock_session):
        storage_host_group_lst \
            = fake_data.fake_storage_host_group_create()
        expected = fake_data.fake_expected_storage_host_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        result = db_api.storage_host_groups_update(ctxt,
                                                   storage_host_group_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_group_delete(self, mock_session):
        storage_host_group_lst \
            = fake_data.fake_storage_host_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_host_group_lst
        result = db_api.storage_host_groups_delete(ctxt,
                                                   storage_host_group_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_storage_host_group_delete_by_storage(self, mock_session):
        storage_host_group_lst \
            = fake_data.fake_storage_host_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = storage_host_group_lst
        result = db_api.storage_host_groups_delete_by_storage(
            ctxt, storage_host_group_lst[0]['storage_id'])
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_groups_create(self, mock_session):
        port_group_lst \
            = fake_data.fake_port_group_create()
        expected = fake_data.fake_expected_port_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.port_groups_create(
            ctxt, port_group_lst)
        utils.validate_db_schema_model(got[0], models.PortGroup)
        utils.validate_db_schema_model(expected[0], models.PortGroup)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_group_update(self, mock_session):
        port_group_lst \
            = fake_data.fake_port_group_create()
        expected = fake_data.fake_expected_port_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        result = db_api.port_groups_update(ctxt, port_group_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_group_delete(self, mock_session):
        port_group_lst \
            = fake_data.fake_port_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = port_group_lst
        result = db_api.port_groups_delete(ctxt, port_group_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_port_group_delete_by_storage(self, mock_session):
        port_group_lst \
            = fake_data.fake_port_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = port_group_lst
        result = db_api.port_groups_delete_by_storage(
            ctxt, port_group_lst[0]['storage_id'])
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_groups_create(self, mock_session):
        volume_group_lst \
            = fake_data.fake_volume_group_create()
        expected = fake_data.fake_expected_volume_groups_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.volume_groups_create(
            ctxt, volume_group_lst)
        utils.validate_db_schema_model(got[0], models.VolumeGroup)
        utils.validate_db_schema_model(expected[0], models.VolumeGroup)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_group_update(self, mock_session):
        volume_group_lst \
            = fake_data.fake_volume_group_create()
        expected = fake_data.fake_expected_volume_groups_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        result = db_api.volume_groups_update(ctxt, volume_group_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_group_delete(self, mock_session):
        volume_group_lst \
            = fake_data.fake_volume_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = volume_group_lst
        result = db_api.volume_groups_delete(ctxt, volume_group_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_volume_group_delete_by_storage(self, mock_session):
        volume_group_lst \
            = fake_data.fake_volume_group_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = volume_group_lst
        result = db_api.volume_groups_delete_by_storage(
            ctxt, volume_group_lst[0]['storage_id'])
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_masking_views_create(self, mock_session):
        masking_view_lst \
            = fake_data.fake_masking_view_create()
        expected = fake_data.fake_expected_masking_views_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        got = db_api.masking_views_create(
            ctxt, masking_view_lst)
        utils.validate_db_schema_model(got[0], models.MaskingView)
        utils.validate_db_schema_model(expected[0], models.MaskingView)
        self.assertDictMatch(got[0], expected[0])

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_masking_view_update(self, mock_session):
        masking_view_lst \
            = fake_data.fake_masking_view_create()
        expected = fake_data.fake_expected_masking_views_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = expected
        result = db_api.masking_views_update(ctxt, masking_view_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_masking_view_delete(self, mock_session):
        masking_view_lst \
            = fake_data.fake_masking_view_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = masking_view_lst
        result = db_api.masking_views_delete(ctxt, masking_view_lst)
        assert result is None

    @mock.patch('delfin.db.sqlalchemy.api.get_session')
    def test_masking_view_delete_by_storage(self, mock_session):
        masking_view_lst \
            = fake_data.fake_masking_view_create()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = masking_view_lst
        result = db_api.masking_views_delete_by_storage(
            ctxt, masking_view_lst[0]['storage_id'])
        assert result is None
