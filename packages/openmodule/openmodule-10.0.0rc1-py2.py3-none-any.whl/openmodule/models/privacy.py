from typing import Optional, List

from openmodule.models.base import ZMQMessage, OpenModuleModel


class AnonymizeMessage(ZMQMessage):
    type: str = "anonymize"
    session_id: str
    vehicle_ids: Optional[List[str]] = []


class AnonymizeRequest(OpenModuleModel):
    session_ids: List[str]


class AnonymizeResponse(OpenModuleModel):
    pass
