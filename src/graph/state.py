from langgraph.graph import MessagesState
from langgraph.graph.message import AnyMessage, add_messages
from typing import Annotated


class MessageState(MessagesState):

    messages: Annotated[list[AnyMessage], add_messages]