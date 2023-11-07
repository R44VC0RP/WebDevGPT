def create_assistants():
    # Create the CodingAI assistant to generate website code
    coding_ai = client.beta.assistants.create(
        name="CodingAI",
        instructions="You will generate HTML, CSS, and JavaScript code based on detailed web development tasks.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview"
    )

    logging.info("CodingAI Assistant Created with ID: %s", coding_ai.id)