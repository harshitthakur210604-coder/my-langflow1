from harxitflow.services.base import Service
from harxitflow.services.factory import ServiceFactory
from harxitflow.services.job_queue.service import JobQueueService


class JobQueueServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(JobQueueService)

    def create(self) -> Service:
        return JobQueueService()
