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

    # if from_id|user_id is not equal to peer_id
    # =>
    # we've got a message from some conversation
    from_conversation: Optional[bool] = None

class MessageNew(MessageBase):
    text: str
    from_id: int
    fwd_messages: List[Any]
    payload: str = None


class MessageEvent(MessageBase):
    user_id: int
    payload: Dict[str, Any]


def serialize_message(data: dict) -> Union[MessageNew, MessageEvent, None]:
    if data["type"] == "message_new":
        peer_id = data["object"]["message"]["peer_id"]
        from_id = data["object"]["message"]["from_id"]
        return MessageNew(
            type = data["type"],
            from_conversation=peer_id != from_id,
            **data["object"]["message"]
        )
    elif data["type"] == "message_event":
        peer_id = data["object"]["peer_id"]
        user_id = data["object"]["user_id"]
        return MessageEvent(
            type = data["type"],
            from_conversation=peer_id != user_id,
            **data["object"]
        )
