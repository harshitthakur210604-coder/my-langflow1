from typing_extensions import override

from harxitflow.services.factory import ServiceFactory
from harxitflow.services.flow_events.service import FlowEventsService


class FlowEventsServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(FlowEventsService)

    @override
    def create(self):
        return FlowEventsService()
