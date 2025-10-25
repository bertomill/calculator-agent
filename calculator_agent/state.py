from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    """
    Defines the state structure for our calculator agent.
    
    This is like a blueprint for what information the agent remembers:
    - messages: The conversation history
    - llm_calls: How many times we've called the language model
    """
    # List of all messages in the conversation
    # Annotated with operator.add means new messages are appended, not replaced
    messages: Annotated[list[AnyMessage], operator.add]
    
    # Counter to track how many times we've called the LLM
    llm_calls: int

def create_initial_state(messages: list[AnyMessage] = None) -> MessagesState:
    """
    Create the initial state for a new conversation.
    
    Args:
        messages: Initial messages (usually just the user's question)
        
    Returns:
        MessagesState: The initial state with empty conversation and zero LLM calls
    """
    if messages is None:
        messages = []
    
    return {
        "messages": messages,
        "llm_calls": 0
    }

def get_state_info(state: MessagesState) -> dict:
    """
    Get a summary of the current state for debugging.
    
    Args:
        state: The current agent state
        
    Returns:
        dict: Summary information about the state
    """
    return {
        "message_count": len(state["messages"]),
        "llm_calls": state["llm_calls"],
        "last_message_type": type(state["messages"][-1]).__name__ if state["messages"] else "None"
    }