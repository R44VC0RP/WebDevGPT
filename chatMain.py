from openai import OpenAI
import json

# Initialize your OpenAI API key
client = OpenAI()
# Message memories to store conversation histories for multiple AI agents
messageMemories = {}

functionDefinitions = {
            "name": "create_website",
            "description": "Create a simple website",
            "parameters": {
                "type": "object",
                "properties": {
                    "html": {"type": "string", "description": "HTML code"},
                    "css": {"type": "string", "description": "CSS code"},
                    "javascript": {"type": "string", "description": "JavaScript code"},
                },
                "required": ["html", "css", "javascript"]
            }
        }, {
            "name": "messageCodingAI",
            "description": "Send a message to a coding AI",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Message text"},
                },
                "required": ["message"]
            }
        }

# Python function corresponding to the OpenAI callable function "create_website"
def create_website(html, css, javascript):
    # Placeholder for website creation logic
    return "Website created with provided HTML, CSS, and JavaScript."

# Python function corresponding to the OpenAI callable function "messageCodingAI"
def messageCodingAI(message):
    # Placeholder for interacting with a coding-oriented AI
    return f"Response from coding AI to the message: {message}"

# Function to manage message histories
def message_management(agent_id, action, new_message=None):
    if agent_id not in messageMemories:
        messageMemories[agent_id] = []

    if action == "add" and new_message:
        messageMemories[agent_id].append({"role": "user", "content": new_message})
    elif action == "funcadd" and new_message:
        messageMemories[agent_id].append({"role": "function", "content": None, "function_call": new_message})
    elif action == "listall":
        return messageMemories[agent_id]
    elif action == "getlast":
        return messageMemories[agent_id][-1] if messageMemories[agent_id] else None

    return messageMemories[agent_id]

# Function to send a new message and get the completion
def send_message(agent_id, new_message):
    message_management(agent_id, "add", new_message)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messageMemories[agent_id],
        functions=functionDefinitions,
        function_call="auto"
    )

    choice = response.choices[0]
    print(choice.message)
    if 'function_call' in choice.message:
        function_name = choice.message['function_call']['name']
        arguments = json.loads(choice.message['function_call']['arguments'])
        
        local_functions = {
            'create_website': create_website,
            'messageCodingAI': messageCodingAI,
        }

        if function_name in local_functions:
            functionResponse = local_functions[function_name](**arguments)
            message_management(agent_id, "funcadd", choice.message['function_call'])
        else:
            raise ValueError("Function name not recognized.")
    
    return choice.message["content"]

# Example Usage
completion = send_message('agent_1', "Please create a basic webpage with a welcome message.")
print(completion)
completion = send_message('agent_2', "Can you write a code snippet to reverse a string?")
print(completion)