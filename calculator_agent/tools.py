from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divides the first integer by the second integer."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Create a list of all available tools
TOOLS = [add, multiply, divide]

# Create a dictionary for quick tool lookup
TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}