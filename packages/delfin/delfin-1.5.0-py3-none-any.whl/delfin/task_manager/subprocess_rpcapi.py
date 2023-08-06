# Copyright 2021 The SODA Authors.
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

"""
Client side of the subprocess metrics collection manager RPC API.
"""

import oslo_messaging as messaging
from oslo_config import cfg

from delfin import rpc

CONF = cfg.CONF


class SubprocessAPI(object):
    """Client side of the subprocess metrics manager collection rpc API.

    API version history:

        1.0 - Initial version.
    """

    RPC_API_VERSION = '1.0'

    def __init__(self):
        super(SubprocessAPI, self).__init__()
        self.target = messaging.Target(topic=CONF.host,
                                       version=self.RPC_API_VERSION)
        self.client = rpc.get_client(self.target,
                                     version_cap=self.RPC_API_VERSION)

    def get_client(self, topic):
        target = messaging.Target(topic=topic,
                                  version=self.RPC_API_VERSION)
        return rpc.get_client(target, version_cap=self.RPC_API_VERSION)

    def assign_job_local(self, context, task_id, executor):
        rpc_client = self.get_client(str(executor))
        call_context = rpc_client.prepare(topic=str(executor), version='1.0',
                                          fanout=False)
        return call_context.cast(context, 'assign_job_local',
                                 task_id=task_id)

    def remove_job_local(self, context, task_id, executor):
        rpc_client = self.get_client(str(executor))
        call_context = rpc_client.prepare(topic=str(executor), version='1.0',
                                          fanout=False)
        return call_context.cast(context, 'remove_job_local',
                                 task_id=task_id)

    def assign_failed_job_local(self, context, failed_task_id, executor):
        rpc_client = self.get_client(str(executor))
        call_context = rpc_client.prepare(topic=str(executor), version='1.0',
                                          fanout=False)
        return call_context.cast(context, 'assign_failed_job_local',
                                 failed_task_id=failed_task_id)

    def remove_failed_job_local(self, context, failed_task_id, executor):
        rpc_client = self.get_client(str(executor))
        call_context = rpc_client.prepare(topic=str(executor), version='1.0',
                                          fanout=False)
        return call_context.cast(context, 'remove_failed_job_local',
                                 failed_task_id=failed_task_id)
