from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, ToolCall
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from langgraph.func import entrypoint, task

from .model import setup_model

@task
def call_llm(messages: list[BaseMessage]):
    """
    LLM decides whether to call a tool or not.
    """
    _, model_with_tools, _ = setup_model()
    
    return model_with_tools.invoke(
        [
            SystemMessage(
                content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
            )
        ]
        + messages
    )

@task
def call_tool(tool_call: ToolCall):
    """
    Performs a single tool call.
    """
    _, _, tools_by_name = setup_model()
    tool = tools_by_name[tool_call["name"]]
    return tool.invoke(tool_call)

@entrypoint()
def functional_agent(messages: list[BaseMessage]):
    """
    The main agent function using the Functional API.
    """
    # Start by calling the LLM with the initial messages
    model_response = call_llm(messages).result()

    # Keep looping until the LLM doesn't want to use any more tools
    while True:
        # If the LLM doesn't want to use tools, we're done
        if not model_response.tool_calls:
            break

        # Execute all the tools the LLM wants to use
        tool_result_futures = [
            call_tool(tool_call) for tool_call in model_response.tool_calls
        ]
        
        # Wait for all tool results to complete
        tool_results = [fut.result() for fut in tool_result_futures]
        
        # Add the LLM's response and tool results to the conversation
        messages = add_messages(messages, [model_response, *tool_results])
        
        # Ask the LLM what to do next with the new information
        model_response = call_llm(messages).result()

    # Add the final response to the conversation
    messages = add_messages(messages, model_response)
    return messages

def create_functional_agent():
    """
    Create a functional agent that can be used like the graph agent.
    """
    return functional_agent

def stream_agent(messages: list[BaseMessage]):
    """
    Stream the agent's responses as they're generated.
    """
    for chunk in functional_agent.stream(messages, stream_mode="updates"):
        yield chunk