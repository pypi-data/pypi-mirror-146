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

import six
from oslo_config import cfg
from oslo_log import log

from delfin import db
from delfin import exception
from delfin.common.constants import TelemetryJobStatus, TelemetryCollection
from delfin.db.sqlalchemy.models import FailedTask
from delfin.db.sqlalchemy.models import Task
from delfin.i18n import _
from delfin.task_manager.scheduler import schedule_manager
from delfin.task_manager.tasks.telemetry import PerformanceCollectionTask
from delfin.task_manager import metrics_rpcapi as metrics_task_rpcapi

LOG = log.getLogger(__name__)
CONF = cfg.CONF


class FailedPerformanceCollectionHandler(object):
    def __init__(self, ctx, failed_task_id, storage_id, args, job_id,
                 retry_count, start_time, end_time, executor):
        self.ctx = ctx
        self.failed_task_id = failed_task_id
        self.retry_count = retry_count
        self.storage_id = storage_id
        self.job_id = job_id
        self.args = args
        self.start_time = start_time
        self.end_time = end_time
        self.metrics_task_rpcapi = metrics_task_rpcapi.TaskAPI()
        self.scheduler_instance = \
            schedule_manager.SchedulerManager().get_scheduler()
        self.result = TelemetryJobStatus.FAILED_JOB_STATUS_INIT
        self.executor = executor

    @staticmethod
    def get_instance(ctx, failed_task_id):
        failed_task = db.failed_task_get(ctx, failed_task_id)
        task = db.task_get(ctx, failed_task[FailedTask.task_id.name])
        return FailedPerformanceCollectionHandler(
            ctx,
            failed_task[FailedTask.id.name],
            task[Task.storage_id.name],
            task[Task.args.name],
            failed_task[FailedTask.job_id.name],
            failed_task[FailedTask.retry_count.name],
            failed_task[FailedTask.start_time.name],
            failed_task[FailedTask.end_time.name],
            failed_task[FailedTask.executor.name],
        )

    def __call__(self):
        # Upon periodic job callback, if storage is already deleted or soft
        # deleted,do not proceed with failed performance collection flow
        try:
            failed_task = db.failed_task_get(self.ctx, self.failed_task_id)
            if failed_task["deleted"]:
                LOG.debug('Storage %s getting deleted, ignoring '
                          'performance collection cycle for failed task id %s.'
                          % (self.storage_id, self.failed_task_id))
                return
        except exception.FailedTaskNotFound:
            LOG.debug('Storage %s already deleted, ignoring '
                      'performance collection cycle for failed task id %s.'
                      % (self.storage_id, self.failed_task_id))
            return

        self.retry_count = self.retry_count + 1
        try:
            telemetry = PerformanceCollectionTask()
            status = telemetry.collect(self.ctx, self.storage_id, self.args,
                                       self.start_time, self.end_time)

            if not status:
                raise exception.TelemetryTaskExecError()
        except Exception as e:
            LOG.error(e)
            msg = _("Failed to collect performance metrics for storage "
                    "id:{0}, reason:{1}".format(self.storage_id,
                                                six.text_type(e)))
            LOG.error(msg)
        else:
            LOG.info("Successfully completed Performance metrics collection "
                     "for storage id :{0} ".format(self.storage_id))
            self.result = TelemetryJobStatus.FAILED_JOB_STATUS_SUCCESS
            self._stop_task()
            return

        if self.retry_count >= TelemetryCollection.MAX_FAILED_JOB_RETRY_COUNT:
            msg = _(
                "Failed to collect performance metrics of task instance "
                "id:{0} for start time:{1} and end time:{2} with "
                "maximum retry. Giving up on "
                "retry".format(self.failed_task_id, self.start_time,
                               self.end_time))
            LOG.error(msg)
            self._stop_task()
            return

        self.result = TelemetryJobStatus.FAILED_JOB_STATUS_RETRYING
        db.failed_task_update(self.ctx, self.failed_task_id,
                              {FailedTask.retry_count.name: self.retry_count,
                               FailedTask.result.name: self.result})

    def _stop_task(self):
        db.failed_task_update(self.ctx, self.failed_task_id,
                              {FailedTask.retry_count.name: self.retry_count,
                               FailedTask.result.name: self.result})
        self.metrics_task_rpcapi.remove_failed_job(self.ctx,
                                                   self.failed_task_id,
                                                   self.executor)
