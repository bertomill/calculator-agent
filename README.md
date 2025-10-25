# Calculator Agent

A LangGraph-based AI agent that can perform arithmetic operations using either the Graph API or Functional API approach.

## 🎯 What This Agent Does

This agent can:
- **Add numbers** (e.g., "Add 3 and 4" → 7)
- **Multiply numbers** (e.g., "Multiply 5 by 6" → 30)  
- **Divide numbers** (e.g., "Divide 20 by 4" → 5)
- **Handle complex expressions** by breaking them down into steps

## 🏗️ Project Structure

---


## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run the Agent
```bash
python 06_main.py
```

## 🔧 How It Works

### Graph API Approach
- **Visual Flow**: The agent is built as a graph of nodes and edges
- **Explicit State**: Clear definition of what data the agent tracks
- **Easy Debugging**: You can see exactly how the agent flows from step to step

### Functional API Approach  
- **Python Control Flow**: Uses standard loops and conditionals
- **Streaming Support**: Can show results as they're generated
- **Familiar Patterns**: More intuitive for developers used to standard Python

## 📚 Learning Path

Read the files in order to understand how the agent works:

1. **01_tools.py** - Start here to see the basic arithmetic functions
2. **02_model.py** - Learn how the AI model is configured
3. **03_state.py** - Understand how the agent remembers conversations
4. **04_graph_api.py** - See the graph-based approach
5. **05_functional_api.py** - See the function-based approach
6. **06_main.py** - Learn how to run and test the agent

## 🧪 Testing the Agent

The agent comes with example questions:
- "Add 3 and 4"
- "Multiply 5 by 6" 
- "Divide 20 by 4"

You can also ask your own questions like:
- "What is 15 plus 27?"
- "Calculate 8 times 9"
- "Divide 100 by 5"

## 🔍 Key Concepts

- **Tools**: Functions the AI can use (add, multiply, divide)
- **State**: What the agent remembers during a conversation
- **LLM Calls**: How many times the AI "thinks" about the problem
- **Message Flow**: How information flows between user, AI, and tools

## 🤔 Which Approach Should I Use?

**Use Graph API when:**
- You want to see the agent's flow visually
- Building complex, multi-step workflows
- You need explicit state management
- Working with teams that benefit from clear structure

**Use Functional API when:**
- You prefer standard Python patterns
- You want streaming capabilities
- Building simpler agents
- You want to get started quickly

## 🐛 Troubleshooting

**Common Issues:**
- **Missing API Key**: Make sure `ANTHROPIC_API_KEY` is set
- **Import Errors**: Run `pip install -r requirements.txt`
- **Tool Errors**: Check that all arithmetic functions are working

**Debug Tips:**
- Use the comparison mode to test both approaches
- Check the LLM call counter to see how many steps the agent took
- Look at the conversation history to understand the flow

## 📖 Next Steps

Once you understand this basic agent, you can:
- Add more arithmetic operations (subtract, power, etc.)
- Create more complex agents with multiple tools
- Build agents that can handle different types of problems
- Integrate with external APIs and databases

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new arithmetic operations
- Improve the error handling
- Add more example questions
- Create better documentation
