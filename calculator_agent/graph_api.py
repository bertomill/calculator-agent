from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from typing import Literal

from .state import MessagesState
from .model import setup_model

def create_llm_node():
    """
    Create the LLM node that decides whether to use tools or respond directly.
    """
    model, model_with_tools, tools_by_name = setup_model()
    
    def llm_call(state: MessagesState):
        """
        LLM decides whether to call a tool or not.
        """
        return {
            "messages": [
                model_with_tools.invoke(
                    [
                        SystemMessage(
                            content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                        )
                    ]
                    + state["messages"]
                )
            ],
            "llm_calls": state.get('llm_calls', 0) + 1
        }
    
    return llm_call

def create_tool_node():
    """
    Create the tool node that executes the selected arithmetic operation.
    """
    _, _, tools_by_name = setup_model()
    
    def tool_node(state: MessagesState):
        """
        Performs the tool call.
        """
        result = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        return {"messages": result}
    
    return tool_node

def create_should_continue():
    """
    Create the conditional logic that decides whether to use tools or end the conversation.
    """
    def should_continue(state: MessagesState) -> Literal["tool_node", END]:
        """
        Decide if we should continue the loop or stop based on whether the LLM made a tool call.
        """
        messages = state["messages"]
        last_message = messages[-1]

        # If the LLM makes a tool call, then perform an action
        if last_message.tool_calls:
            return "tool_node"

        # Otherwise, we stop (reply to the user)
        return END
    
    return should_continue

def create_graph_agent():
    """
    Build and compile the complete calculator agent using the Graph API.
    """
    # Create the individual components
    llm_call = create_llm_node()
    tool_node = create_tool_node()
    should_continue = create_should_continue()
    
    # Build the workflow graph
    agent_builder = StateGraph(MessagesState)

    # Add nodes to the graph
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("tool_node", tool_node)

    # Add edges to connect the nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "llm_call")

    # Compile the agent into an executable form
    agent = agent_builder.compile()
    return agent


def visualize_agent(agent):
    """
    Create a visual representation of the agent's flow.
    """
    from IPython.display import Image
    return Image(agent.get_graph(xray=True).draw_mermaid_png())