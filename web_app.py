from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from calculator_agent.graph_api import create_graph_agent
from calculator_agent.state import create_initial_state
from langchain_core.messages import HumanMessage

# Initialize FastAPI app
app = FastAPI(title="Calculator Agent API")

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Question(BaseModel):
    question: str

# Create the agent once at startup
agent = create_graph_agent()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the HTML interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculator Agent</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            input[type="text"] {
                width: 100%;
                padding: 12px;
                font-size: 16px;
                border: 2px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            button:disabled {
                background-color: #ccc;
                cursor: not-allowed;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                background-color: #f9f9f9;
                border-left: 4px solid #4CAF50;
                border-radius: 5px;
            }
            .error {
                border-left-color: #f44336;
                background-color: #ffebee;
            }
            .conversation {
                margin-top: 10px;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
            }
            .you {
                background-color: #e3f2fd;
                border-left: 3px solid #2196F3;
            }
            .ai, .assistant {
                background-color: #f1f8e9;
                border-left: 3px solid #4CAF50;
            }
            .thinking {
                background-color: #fff3e0;
                border-left: 3px solid #FF9800;
                font-style: italic;
            }
            .calculation {
                background-color: #f3e5f5;
                border-left: 3px solid #9C27B0;
                font-family: monospace;
                font-weight: bold;
            }
            .stats {
                margin-top: 10px;
                font-size: 14px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧮 Calculator Agent</h1>
            <p style="text-align: center; color: #666;">Ask me to add, multiply, or divide numbers!</p>
            
            <input type="text" id="question" placeholder="e.g., Add 3 and 4" />
            <button onclick="askQuestion()">Ask Agent</button>
            
            <div id="result"></div>
        </div>

        <script>
            async function askQuestion() {
                const question = document.getElementById('question').value;
                const resultDiv = document.getElementById('result');
                const button = document.querySelector('button');
                
                if (!question.trim()) {
                    alert('Please enter a question!');
                    return;
                }
                
                // Disable button and show loading
                button.disabled = true;
                button.textContent = 'Thinking...';
                resultDiv.innerHTML = '<div class="result">Processing your question...</div>';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: question })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        displayResult(data);
                    } else {
                        resultDiv.innerHTML = `<div class="result error"><strong>Error:</strong> ${data.detail}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error"><strong>Error:</strong> ${error.message}</div>`;
                } finally {
                    button.disabled = false;
                    button.textContent = 'Ask Agent';
                }
            }
            
            function displayResult(data) {
                const resultDiv = document.getElementById('result');
                let html = '<div class="result">';
                html += '<h3>Conversation:</h3>';
                html += '<div class="conversation">';
                
                data.messages.forEach((msg, idx) => {
                    const className = msg.type.toLowerCase();
                    html += `<div class="message ${className}">`;
                    html += `<strong>${msg.type}:</strong> ${msg.content}`;
                    html += '</div>';
                });
                
                html += '</div>';
                html += `<div class="stats">LLM Calls: ${data.llm_calls}</div>`;
                html += '</div>';
                
                resultDiv.innerHTML = html;
            }
            
            // Allow Enter key to submit
            document.getElementById('question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    askQuestion();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/ask")
async def ask_agent(question: Question):
    """Process a question through the calculator agent"""
    try:
        # Create initial state with the user's question
        initial_messages = [HumanMessage(content=question.question)]
        initial_state = create_initial_state(initial_messages)
        
        # Run the agent
        result = agent.invoke(initial_state)
        
        # Format the response - only show user-friendly messages
        messages = []
        for msg in result["messages"]:
            msg_type = type(msg).__name__
            
            # Skip tool calls in AI messages - only show the final response
            if msg_type == "AIMessage":
                # If it has tool calls, show a thinking indicator
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    messages.append({
                        "type": "AI (thinking)",
                        "content": f"🤔 Using {msg.tool_calls[0]['name']} tool..."
                    })
                else:
                    # Final AI response
                    messages.append({
                        "type": "AI Assistant",
                        "content": msg.content
                    })
            elif msg_type == "HumanMessage":
                messages.append({
                    "type": "You",
                    "content": msg.content
                })
            elif msg_type == "ToolMessage":
                # Show tool result in a friendly way
                messages.append({
                    "type": "Calculation",
                    "content": f"Result: {msg.content}"
                })
        
        return {
            "messages": messages,
            "llm_calls": result["llm_calls"],
            "success": True
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e), "success": False}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
        