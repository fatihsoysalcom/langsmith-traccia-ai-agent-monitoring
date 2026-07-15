import os
import random
from langsmith import Client

# --- Configuration ---
# Replace with your actual LangSmith API key and project name
# You can set these as environment variables for security.
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY", "YOUR_LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "ai-agent-demo")

# --- Mock AI Agent --- 
# This function simulates a simple AI agent that might produce unexpected results.
def simple_ai_agent(user_input):
    """Simulates an AI agent's response, with potential for errors or unexpected output."""
    responses = [
        f"The AI agent processed: '{user_input}'. Everything seems normal.",
        f"Error: The AI agent encountered an issue processing '{user_input}'.",
        f"Warning: The AI agent is experiencing high load. Response for '{user_input}' might be delayed.",
        f"Unexpected: The AI agent generated a strange response for '{user_input}'. Halucination detected!"
    ]
    # Simulate random behavior, including potential issues
    return random.choice(responses)

# --- LangSmith Integration (Observability) ---
# LangSmith client for logging and tracing.
client = Client(api_key=LANGSMITH_API_KEY)

def run_agent_with_langsmith(user_query):
    """Runs the AI agent and logs the interaction using LangSmith."""
    # Start a LangSmith trace for this interaction.
    # This is the core of LangSmith's observability approach.
    with client.trace(inputs={'user_query': user_query}, project_name=LANGSMITH_PROJECT) as trace:
        try:
            # Simulate the agent's execution
            agent_response = simple_ai_agent(user_query)
            
            # Log the agent's output as a tool/LLM call within the trace.
            # This allows detailed inspection of intermediate steps and final results.
            trace.log_output(agent_response)
            
            # If the response indicates an error or unexpected behavior, we can mark the trace.
            if "Error" in agent_response or "Unexpected" in agent_response or "Halucination" in agent_response:
                trace.update(error=True, tags=["potential_issue", "observability_flag"])
            
            return agent_response
        except Exception as e:
            # Log any exceptions that occur during agent execution.
            trace.log_exception(e)
            trace.update(error=True, tags=["exception"])
            return f"An internal error occurred: {e}"

# --- Traccia Integration (Enforcement - Conceptual) ---
# Traccia focuses on active enforcement and guardrails.
# This example will *simulate* a Traccia-like check.
# In a real Traccia implementation, you'd have a separate service or library
# that intercepts calls and applies rules *before* or *during* execution.

def enforce_traccia_like_rules(user_input, agent_response):
    """Simulates Traccia's enforcement by checking for forbidden patterns.
    In a real scenario, this would be more sophisticated and proactive.
    """
    forbidden_keywords = ["infinite loop", "budget exceeded"]
    for keyword in forbidden_keywords:
        if keyword in agent_response.lower():
            print(f"TRACCIA-LIKE ENFORCEMENT: Detected forbidden keyword '{keyword}'. Blocking response.")
            return False # Block the response
    return True # Allow the response

# --- Main Execution --- 
if __name__ == "__main__":
    print("--- AI Agent Demo with Observability (LangSmith) and Simulated Enforcement (Traccia) ---")
    
    # Example queries to test the agent
    queries = [
        "What is the weather today?",
        "Tell me a joke.",
        "Please perform a critical system operation.", # Simulating a potentially problematic query
        "Calculate 2+2."
    ]
    
    for query in queries:
        print(f"\nUser Query: {query}")
        
        # --- LangSmith Observability Part ---
        # Run the agent and capture its output, logging to LangSmith.
        langsmith_response = run_agent_with_langsmith(query)
        print(f"Agent Response (Observed): {langsmith_response}")
        
        # --- Traccia-like Enforcement Part ---
        # Simulate checking the response against predefined rules.
        # This check happens *after* the agent has responded in this simulation,
        # but in Traccia, it would often be *before* or *during* execution.
        if enforce_traccia_like_rules(query, langsmith_response):
            print("Enforcement Check: PASSED. Response is acceptable.")
        else:
            print("Enforcement Check: FAILED. Response was blocked by simulated guardrails.")

    print("\n--- Demo Finished --- ")
    print("Check your LangSmith project for traces: https://smith.langchain.com/")
