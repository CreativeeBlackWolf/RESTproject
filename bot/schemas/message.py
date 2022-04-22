from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel


class MessageEventTypes:
    MESSAGE_NEW = "message_new"
    MESSAGE_EVENT = "message_event"

# TODO: do a message model and serialize them in another files
class MessageBase(BaseModel):
    # response root
    type: str

    # response["object"]
    peer_id: int
    from_id: Optional[int] = None
    user_id: Optional[int] = None

    # if from_id is not equal to peer_id
    # =>
    # we've got a message from some conversation
    # from_conversation: bool = not (from_id == peer_id)

class MessageNew(MessageBase):
    text: str
    fwd_messages: List[Any]


class MessageEvent(MessageBase):
    payload: Dict[str, Any]


def serialize_message(data: dict) -> Union[MessageNew, MessageEvent, None]:
    if data["type"] == "message_new":
        return MessageNew(
            type = data["type"],
            **data["object"]["message"]
        )
    elif data["type"] == "message_event":
        return MessageEvent(
            type = data["type"],
            **data["object"]
        )
