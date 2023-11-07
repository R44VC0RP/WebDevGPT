from openai import OpenAI
import os
import logging
import time
import functions
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", filename="weddevgpt.log")

client = OpenAI()

coding_ai_id_35 = "asst_OO9fuCFGsDtmPhEWJ0Ihz7Zy"
prompt_at_id_35 = "asst_B6yomAvgVF4dbtxJhYXp9Ok6"

prompt_ai_id_4 = "asst_iEBeGcs4FNywyhkdk8SJKiIP"
coding_ai_id_4 = "asst_0vmT1XOEp7PV3s8theanh3PZ"

prompt_ai = prompt_at_id_35
coding_ai = coding_ai_id_35

def threadInit(function):
    logging.info("Initializing Thread")
    if function == "coding":
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Follow the instructions to create a custom website.",
                }
            ]
        )
        logging.info("CodingAI Thread Initialized with ID: %s", thread.id)
    elif function == "prompt":
        thread = client.beta.threads.create()
        logging.info("PromptAI Thread Initialized with ID: %s", thread.id)
    
    return thread.id

codingThreadID = threadInit("coding")
promptThreadID = threadInit("prompt")

def process_run_object(run_object):
    #tool_calls = run_object.get("required_action", {}).get("submit_tool_outputs", {}).get("tool_calls", [])
    tool_calls = run_object.required_action.submit_tool_outputs.tool_calls
    
    for call in tool_calls:
        function_name = call.function.name
        arguments = call.function.arguments
        
        # Based on the function name, decide which Python function to call. Add more elif branches as you add more functions.
        if function_name == "create_website":
            arguments = json.loads(arguments)
            html_code = arguments.get("html_code", "")
            css_code = arguments.get("css_code", "")
            js_code = arguments.get("js_code", None) 

            # Call the create_website function with parameters extracted from the run_object.
            result = functions.create_website(html_code, css_code, js_code)
            print(result)  # Printing for demonstration purposes. In practice, handle the result as needed.

        if function_name == "start_coder":
            arguments = json.loads(arguments)
            message = arguments.get("message", "")
            threadMessage(codingThreadID, message)
            askCodingAI(codingThreadID)
            message = client.beta.threads.messages.list(thread_id=codingThreadID)
            print(message.data.content)
            return message


            

def codingAIThreadObject(threadID):
    logging.info("Retrieving CodingAI Thread Object")
    thread = client.beta.threads.retrieve(thread_id=threadID)
    logging.info("CodingAI Thread Object Retrieved")
    return thread

def threadMessage(threadID, message):
    logging.info("Sending message to thread")
    
    client.beta.threads.messages.create(thread_id=threadID, content=message, role="user")
    logging.info("Message sent to thread")

def askCodingAI(threadID):
    logging.info("Asking CodingAI for a response")
    # Poll the Assistants API for a completed response from an assistant run
    run = client.beta.threads.runs.create(
        thread_id=threadID,
        assistant_id=coding_ai
    )
    while True:
        logging.info("CodingAI response status: %s", run.status)
        if run.status == 'completed':
            logging.info("Received completed response from CodingAI")
            break
        if run.status == 'requires_action':
            logging.info("CodingAI response requires action")

            # Get the action prompt from the run
            runId = run.id
            toolId = run.required_action.submit_tool_outputs.tool_calls[0].id
            print("Tool ID: {} and Run ID: {}".format(toolId, runId))
            process_run_object(run)
            client.beta.threads.runs.submit_tool_outputs(
                run_id=runId,
                thread_id=threadID,
                tool_outputs=[
                    {
                        "tool_call_id": toolId,
                        "output": "success"
                    }
                ]
            )
            logging.info("CodingAI response action submitted")

            time.sleep(1)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
            
        else:
            time.sleep(1)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
    
    logging.info("CodingAI response received")

def askPromptAI(threadID):
    logging.info("Asking PromptAI for a response")
    # Poll the Assistants API for a completed response from an assistant run
    run = client.beta.threads.runs.create(
        thread_id=threadID,
        assistant_id=prompt_ai
    )
    while True:
        logging.info("PromptAI response status: %s", run.status)
        if run.status == 'completed':
            logging.info("Received completed response from CodingAI")
            break
        if run.status == 'requires_action':
            logging.info("PromptAI response requires action")

            # Get the action prompt from the run
            runId = run.id
            toolId = run.required_action.submit_tool_outputs.tool_calls[0].id
            print("Tool ID: {} and Run ID: {}".format(toolId, runId))
            responseFromCodingAI = process_run_object(run)
            client.beta.threads.runs.submit_tool_outputs(
                run_id=runId,
                thread_id=threadID,
                tool_outputs=[
                    {
                        "tool_call_id": toolId,
                        "output": responseFromCodingAI
                    }
                ]
            )
            logging.info("PromptAI response action submitted")

            time.sleep(1)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
            
        else:
            time.sleep(1)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
    
    logging.info("PromptAI response received")
    promptAIresponse = client.beta.threads.messages.list(thread_id=threadID)[-1].value
    print("PromptAI Response: " + promptAIresponse)
    

def main():
    logging.info("Starting main function")
    print("Welcome to WedDevGPT!")
    
    userPrompt = "Create a website for Ryan Vogel that is modern with white bold text and a darker background color." #input("What would you like the website to look like? ")
    threadMessage(promptThreadID, userPrompt)
    askPromptAI(promptThreadID)
    # askCodingAI(codingThreadID)
    # response = codingAIThreadObject(codingThreadID)
    # messages = client.beta.threads.messages.list(thread_id=codingThreadID)
    # for message in messages:
    #     print("Message: " + str(message.content))
    
    logging.info("Main function completed")


if __name__ == "__main__":
    main()
