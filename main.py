import openai
import os
import logging
import time
import functions
import json

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("webdevgpt.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
 
# Set up OpenAI API
client = openai.OpenAI()


# Set up OpenAI API - assistant IDs
coding_ai_id_35 = "asst_OO9fuCFGsDtmPhEWJ0Ihz7Zy"
prompt_at_id_35 = "asst_B6yomAvgVF4dbtxJhYXp9Ok6"

prompt_ai_id_4 = "asst_iEBeGcs4FNywyhkdk8SJKiIP"
coding_ai_id_4 = "asst_0vmT1XOEp7PV3s8theanh3PZ"

prompt_ai = prompt_at_id_35
coding_ai = coding_ai_id_35

def threadInit(function):
    logger.info("Initializing Thread")
    if function == "coding":
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Follow the instructions to create a custom website.",
                }
            ]
        )
        logger.info("CodingAI Thread Initialized with ID: %s", thread.id)
    elif function == "prompt":
        thread = client.beta.threads.create()
        logger.info("PromptAI Thread Initialized with ID: %s", thread.id)
    
    return thread.id

codingThreadID = threadInit("coding")
promptThreadID = threadInit("prompt")
# This initilizes the message threads for coding and promtp AI

def functionCalling(run_object):
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
            #createdImage = functions.webpageImageRender()
            return result # return the result to the calling function.

        if function_name == "start_coder":
            arguments = json.loads(arguments)
            message = arguments.get("message", "")
            modifedMessage = "PromptAI: " + message
            threadMessage(codingThreadID, modifedMessage)
            print("PromptAI: <A> Asking CodingAI to create the 1st draft.")
            message = askCodingAI(codingThreadID) # CodingAI response is returned as a string.
            return message

def threadMessage(threadID, message="placeholder", action="create"):
    if action == "create":
        client.beta.threads.messages.create(thread_id=threadID, content=message, role="user")
        logger.info("Message: %s sent to thread %s", message, threadID)
        return "Message sent to thread"
    elif action == "list":
        logger.info("Listing messages from thread")
        messages = client.beta.threads.messages.list(threadID)
        messageList = messages.data[0].content
        logger.info("Messages listed from thread")
        return messageList
    elif action == "newest":
        logger.info("Getting newest message from thread")
        messages = client.beta.threads.messages.list(threadID)
        newestMessage = messages.data[0].content[0].text.value
        logger.info("Newest message from thread retrieved")
        return newestMessage

def askCodingAI(threadID):
    logger.info("Asking CodingAI for a response")
    # 1. Create a run with the CodingAI assistant thread.
    run = client.beta.threads.runs.create(thread_id=threadID, assistant_id=coding_ai)
    # 2. Poll the Assistants API for a completed response from an assistant run
    while True:
        logger.info("CodingAI response status: %s", run.status)
        if run.status == 'completed':
            # 4. Get the final message response from the run.
            codingAIresponse = threadMessage(threadID=threadID, action="newest") # This gets the newest message from the thread.
            print("CodingAI: " + codingAIresponse)
            logger.info("CodingAI response: " + codingAIresponse)
            return codingAIresponse
        if run.status == 'requires_action':
            print("CodingAI: <A> Creating the website.")
            logger.info("CodingAI response requires action")
            # 3. The CodingAI assistant has a required action. In this case, it is a tool call.
            runId = run.id
            toolId = run.required_action.submit_tool_outputs.tool_calls[0].id
            # 4. This gets the runID and the toolID so that it can be used to update the action once the "websiteCreation" function is called and the image of the rendered website is returned.
            logger.info("Tool ID: {} and Run ID: {}".format(toolId, runId))
            websiteCreationResponse = functionCalling(run) # This calls the function that will create the website and return the image of the rendered website.
            logger.info("Website creation response: " + websiteCreationResponse)
            client.beta.threads.runs.submit_tool_outputs(
                run_id=runId,
                thread_id=threadID,
                tool_outputs=[
                    {
                        "tool_call_id": toolId,
                        "output": "success",
                        # This will submit a tool (update) with the toolID and the output will be a link (string) to the image of the rendered website. This will be used to update the action.
                    }
                ]
            )
            time.sleep(.5)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
        else:
            time.sleep(.5)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
    
def askPromptAI(threadID):
    logger.info("Asking PromptAI for a response")
    # 1. Create a run with the PromptAI assistant thread.
    run = client.beta.threads.runs.create(thread_id=threadID, assistant_id=prompt_ai)
    # 2. Poll the Assistants API for a completed response from an assistant run
    while True:
        logger.info("PromptAI response status: %s", run.status)
        if run.status == 'completed':
            # 3. The PromptAI assistant has completed and returned a response.
            # 4. Get the final message response from the run.
            promptAIresponse = threadMessage(threadID=threadID, action="newest")
            print("PromptAI: " + promptAIresponse)
            logger.info("Received completed response from CodingAI | >>> " + promptAIresponse)
            break
        if run.status == 'requires_action':
            logger.info("PromptAI response requires action")
            # Get the action prompt from the run
            runId = run.id
            toolId = run.required_action.submit_tool_outputs.tool_calls[0].id
            logger.info("Tool ID: {} and Run ID: {}".format(toolId, runId))
            responseFromCodingAI = functionCalling(run)
            
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
            logger.info("PromptAI response action submitted")
            time.sleep(1)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
            if run.status == 'completed':
                modifiedResponse = "CodingAI: " + responseFromCodingAI
                threadMessage(threadID=threadID, message=modifiedResponse, action="create")
        else:
            time.sleep(1)  # wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadID)
    
def threadObjectTestRetrevial(threadID):
    logger.info("Retrieving thread object")
    threadObject = client.beta.threads.messages.list(threadID)
    print("Thread Object: " + str(threadObject.data[0].content[0].text.value))
    
    logger.info("Thread object retrieved")
    return threadObject

def main():
    logger.info("Starting main function")
    print("Welcome to WedDevGPT!")

    #threadObjectTestRetrevial("thread_cBbmbQZPfIXHlE60Kj8DMNc2")

    # userPrompt = "Create a website for Ryan Vogel that is modern with white bold text and a darker background color." #input("What would you like the website to look like? ")
    # threadMessage(threadID=promptThreadID, message=userPrompt, action="create")
    # askPromptAI(promptThreadID)
    
    
    
    # askCodingAI(codingThreadID)
    # response = codingAIThreadObject(codingThreadID)
    # messages = client.beta.threads.messages.list(thread_id=codingThreadID)
    # for message in messages:
    #     print("Message: " + str(message.content))
    
    logger.info("Main function completed")


if __name__ == "__main__":
    main()
