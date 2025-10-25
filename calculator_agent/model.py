from dotenv import load_dotenv
load_dotenv(".env.local")

from langchain.chat_models import init_chat_model
from calculator_agent.tools import TOOLS, TOOLS_BY_NAME

def setup_model():
    """
    Initialize and configure the Claude language model with our arithmetic tools.
    
    Returns:
        tuple: (model, model_with_tools, tools_by_name)
    """
    # Initialize Claude Sonnet 4.5 with temperature=0 for consistent results
    model = init_chat_model(
        "anthropic:claude-sonnet-4-5",
        temperature=0  # Low temperature for consistent, deterministic responses
    )
    
    # Connect our arithmetic tools to the model
    model_with_tools = model.bind_tools(TOOLS)
    
    return model, model_with_tools, TOOLS_BY_NAME

def get_model_info():
    """
    Get information about the configured model.
    
    Returns:
        dict: Model configuration details
    """
    return {
        "model_name": "anthropic:claude-sonnet-4-5",
        "temperature": 0,
        "available_tools": [tool.name for tool in TOOLS],
        "tool_count": len(TOOLS)
    }