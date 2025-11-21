import os
import json
import math # Used for the distance calculation
from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Initialize Gemini client
# NOTE: Ensure you have GEMINI_API_KEY set in your .env file
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# --- Tool Function Implementation ---

def calculate_distance(x1: float, y1: float, x2: float, y2: float):
    """
    Calculates the Euclidean distance between two 2D points (x1, y1) and (x2, y2).
    
    This calculation uses the distance formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    try:
        # Calculate the difference in coordinates
        dx = x2 - x1
        dy = y2 - y1
        
        # Apply the Pythagorean theorem (Euclidean Distance)
        distance = math.sqrt(dx**2 + dy**2)
        
        # Return the result
        return {
            "distance": distance,
            "units": "arbitrary_units",
            "point1": f"({x1}, {y1})",
            "point2": f"({x2}, {y2})"
        }
    except Exception as e:
        return {"error": f"Calculation failed. Details: {str(e)}"}


# --- Tool Definitions ---

# Define tools for Gemini
tools_schema = [
    {
        "name": "calculate_distance",
        "description": "Calculates the straight-line distance between two points (x1, y1) and (x2, y2) in a 2D coordinate system. Use this when the user asks for distance or comparison of distances.",
        "parameters": {
            "type": "object",
            "properties": {
                "x1": {"type": "number", "description": "The x-coordinate of the first point."},
                "y1": {"type": "number", "description": "The y-coordinate of the first point."},
                "x2": {"type": "number", "description": "The x-coordinate of the second point."},
                "y2": {"type": "number", "description": "The y-coordinate of the second point."},
            },
            "required": ["x1", "y1", "x2", "y2"],
        },
    },
]

available_functions = {
    "calculate_distance": calculate_distance,
}

# Configure tools for Gemini
gemini_tools = types.Tool(function_declarations=tools_schema)


class GeminiReactAgent:
    """A ReAct (Reason and Act) agent using Google Gemini."""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.max_iterations = 10
        
    def run(self, initial_query: str) -> str:
        """
        Run the ReAct loop until we get a final answer.
        """
        iteration = 0
        # Start with a Content object for the user query
        contents = [types.Content(role="user", parts = [types.Part.from_text(text=initial_query)])] 
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Create config with tools
            config = types.GenerateContentConfig(tools=[gemini_tools])
            
            # Call the LLM
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )
            
            print(f"LLM Response: {response}")
            
            # Check if there are function calls
            function_calls = response.function_calls if response.function_calls else []
            has_function_calls = len(function_calls) > 0
            
            if has_function_calls:
                # Add model's request to contents for context
                contents.append(response.candidates[0].content)
                
                # Process ALL function calls
                function_responses = []
                for function_call in function_calls:
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    print(f"Executing tool: {function_name}({function_args})")
                    
                    # Call the function
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)
                    
                    print(f"Tool result: {function_response}")
                    
                    # Create function response for Gemini format
                    func_response = types.FunctionResponse(
                        name=function_name,
                        response=function_response
                    )
                    function_responses.append(func_response)
                
                # Add all function responses as a single content part
                # The role for function responses is 'tool'
                contents.append(types.Content(
                    role="tool", 
                    parts=[types.Part(function_response=fr) for fr in function_responses]
                ))
                
                # Continue the loop to get the next response
                continue
                
            else:
                # No function calls - we have our final answer
                final_content = response.text
                
                print(f"\n {final_content}")
                return final_content
        
        # If we hit max iterations, return an error
        return "Error: Maximum iterations reached without getting a final answer."


def main():
    # Create a ReAct agent
    agent = GeminiReactAgent()
    
    # --- Example 1: Single calculation query ---
    print("=== Example 1: Single Distance Calculation ===")
    result1 = agent.run("What is the distance between the point (3, 4) and the origin (0, 0)?")
    print(f"\nResult: {result1}")
    
    # --- Example 2: Sequential Reasoning (LLM must compare multiple results) ---
    print("\n\n=== Example 2: Distance Comparison Query ===")
    # The LLM must call the tool twice and compare the distances to answer this question.
    query = "Which distance is greater: the distance from (10, 5) to (2, 9), or the distance from (1, 1) to (1, 10)? Show the calculations."
    result2 = agent.run(query)
    print(f"\nResult: {result2}")
    

if __name__ == "__main__":
    main()