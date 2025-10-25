import os
import sys

# Ensure the project root (parent of this package directory) is on sys.path
# so that `calculator_agent` can be imported when running this file directly.
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(PACKAGE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from langchain_core.messages import HumanMessage
from calculator_agent.state import create_initial_state
from calculator_agent.graph_api import create_graph_agent, visualize_agent
from calculator_agent.functional_api import create_functional_agent, stream_agent

def run_graph_agent(question: str):
    """
    Run the calculator agent using the Graph API approach.
    """
    print("🤖 Running Graph API Agent...")
    print(f"Question: {question}")
    print("-" * 50)
    
    # Create the agent
    agent = create_graph_agent()
    
    # Prepare the initial state
    initial_messages = [HumanMessage(content=question)]
    initial_state = create_initial_state(initial_messages)
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    # Display the results
    print("Conversation:")
    for i, message in enumerate(result["messages"]):
        print(f"{i+1}. {type(message).__name__}: {message.content}")
    
    print(f"\nTotal LLM calls: {result['llm_calls']}")
    return result

def run_functional_agent(question: str):
    """
    Run the calculator agent using the Functional API approach.
    """
    print("🤖 Running Functional API Agent...")
    print(f"Question: {question}")
    print("-" * 50)
    
    # Create the agent
    agent = create_functional_agent()
    
    # Prepare the initial messages
    initial_messages = [HumanMessage(content=question)]
    
    # Run the agent
    result = agent(initial_messages)
    
    # Display the results
    print("Conversation:")
    for i, message in enumerate(result):
        print(f"{i+1}. {type(message).__name__}: {message.content}")
    
    return result

def run_streaming_agent(question: str):
    """
    Run the calculator agent with streaming output.
    """
    print("🤖 Running Streaming Agent...")
    print(f"Question: {question}")
    print("-" * 50)
    
    # Prepare the initial messages
    initial_messages = [HumanMessage(content=question)]
    
    # Stream the results
    for chunk in stream_agent(initial_messages):
        print(f"Update: {chunk}")
        print()

def compare_approaches(question: str):
    """
    Run both Graph API and Functional API approaches and compare them.
    """
    print("🔄 Comparing Graph API vs Functional API...")
    print(f"Question: {question}")
    print("=" * 60)
    
    # Run Graph API
    print("\n📊 GRAPH API RESULTS:")
    graph_result = run_graph_agent(question)
    
    print("\n" + "=" * 60)
    
    # Run Functional API
    print("\n⚡ FUNCTIONAL API RESULTS:")
    functional_result = run_functional_agent(question)
    
    print("\n" + "=" * 60)
    print("✅ Both approaches should produce the same result!")

def main():
    """
    Main function to demonstrate the calculator agent.
    """
    print("🧮 Calculator Agent Demo")
    print("=" * 40)
    
    # Example questions
    questions = [
        "Add 3 and 4",
        "Multiply 5 by 6",
        "Divide 20 by 4"
    ]
    
    # Choose which approach to use
    approach = input("Choose approach (graph/functional/streaming/compare): ").lower()
    
    for question in questions:
        print(f"\n{'='*60}")
        
        if approach == "graph":
            run_graph_agent(question)
        elif approach == "functional":
            run_functional_agent(question)
        elif approach == "streaming":
            run_streaming_agent(question)
        elif approach == "compare":
            compare_approaches(question)
        else:
            print("Invalid approach. Using Graph API by default.")
            run_graph_agent(question)
        
        input("\nPress Enter to continue to next question...")

if __name__ == "__main__":
    main()