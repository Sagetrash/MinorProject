import asyncio
from dataclasses import dataclass
from typing import AsyncIterator, List, Literal, Any, Optional
from google.genai import types
from config.settings import AppConfig
from config.models import ModelRegistry
from agent.models import GeminiProvider, LLMResponse
from functions.function_map import callFunction
from functions.schemas import avail_functions

@dataclass
class AgentStep:
    step_type: Literal["user", "function", "response"]
    content: str
    metadata: dict = None

class AgentEngine:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.history: List[types.Content] = []

    async def run(self, prompt: str) -> AsyncIterator[AgentStep]:
        config = self.registry.get_config()
        active_model = self.registry.get_active_model()
        
        if not active_model:
            yield AgentStep("response", "No active model configured. Please add one in settings (Ctrl+M).")
            return

        # Initialize provider
        if active_model.provider == "GEMINI":
            provider = GeminiProvider(active_model)
        else:
            yield AgentStep("response", f"Provider {active_model.provider} not yet implemented.")
            return

        # Start conversation
        self.history = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        yield AgentStep("user", prompt)

        for i in range(config.max_iterations):
            # Use run_in_executor for synchronous API calls
            loop = asyncio.get_event_loop()
            try:
                response = await loop.run_in_executor(
                    None, 
                    lambda: provider.generate_content(
                        prompt=prompt if not self.history else None, 
                        tools=avail_functions, 
                        history=self.history,
                        system_prompt=config.system_prompt
                    )
                )
            except Exception as e:
                yield AgentStep("response", f"API Error: {str(e)}")
                return

            # Add assistant response to history
            # We must record the model's turn (even if it only contains function calls) 
            # to maintain the correct turn-taking sequence for the API.
            if response.text:
                model_content = types.Content(
                    role="model", 
                    parts=[types.Part(text=response.text)]
                )
                self.history.append(model_content)
            elif response.function_calls:
                # Only add function calls to history if there's actually content
                model_content = types.Content(
                    role="model", 
                    parts=[types.Part(function_call=call) for call in response.function_calls]
                )
                self.history.append(model_content)
            
            # Handle function calls
            if response.function_calls:
                function_results = []
                for call in response.function_calls:
                    yield AgentStep("function", f"Calling {call.name}...", {"function": call.name, "args": call.args})
                    
                    # Execute function with error handling
                    try:
                        result_content = callFunction(call, config.working_directory, verbose=False)
                        
                        # Extract the actual result string for the UI
                        res_text = result_content.parts[0].function_response.response.get("result", "No result")
                        yield AgentStep("function", f"Result from {call.name}: {res_text}", {"function": call.name, "result": res_text})
                        
                        function_results.append(result_content.parts[0])
                    except Exception as e:
                        yield AgentStep("function", f"Error in {call.name}: {str(e)}", {"function": call.name, "error": str(e)})
                        # Still add an error result to keep the conversation flowing
                        function_results.append(types.Part(function_response=types.FunctionResponse(
                            name=call.name,
                            response={"result": f"Error: {str(e)}"}
                        )))
                
                # Add tool response to history
                self.history.append(types.Content(role="tool", parts=function_results))
            else:
                # No more function calls, return final text
                if response.text:
                    yield AgentStep("response", response.text, {"usage": response.usage})
                else:
                    yield AgentStep("response", "Agent finished without a final response.")
                break
        else:
            yield AgentStep("response", "Reached maximum iterations limit.")
