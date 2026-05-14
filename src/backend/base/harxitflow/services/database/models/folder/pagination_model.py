from fastapi_pagination import Page

from harxitflow.helpers.base_model import BaseModel
from harxitflow.services.database.models.flow.model import FlowRead
from harxitflow.services.database.models.folder.model import FolderRead


class FolderWithPaginatedFlows(BaseModel):
    folder: FolderRead
    flows: Page[FlowRead]
