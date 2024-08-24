"""display chatbot"""

import json
from..templates import template
from .. import styles
import requests
from decouple import config
import reflex as rx
import sys
import os
import re
import time
from openai import AzureOpenAI


# Add the top-level project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

AZURE_OPENAI_API_KEY = config("AZURE_OPENAI_API_KEY", cast=str, default=None)
AZURE_OPENAI_ENDPOINT = config("AZURE_OPENAI_ENDPOINT", cast=str, default=None)

vector_store_id = "vs_zUxocP6ymEEb039iCnBTLjaR"

is_loading = False

PROMPT = """**Instructions:** 

You are tasked with answering questions based strictly on the provided banking data. Your responses must adhere exactly to the information given, with no deviation, interpretation, or addition. If a detail is not mentioned in the provided files, you must explicitly state that the information is not provided. Also mention the exact details of what is contained in a particular segment if it is mentioned in the answer and how it relates to the question asked.

The question is:
"""

def initialize_vector_store(vector_store_id):
    client = AzureOpenAI(
        api_key=(AZURE_OPENAI_API_KEY),
        api_version="2024-05-01-preview",
        azure_endpoint=(AZURE_OPENAI_ENDPOINT)
    )
    
    vector_store = client.beta.vector_stores.retrieve(vector_store_id=vector_store_id)

    # List all .txt files in the specified directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    folder_path = os.path.join(project_root, "azure", "RBI_Guidelines_Documents")
    document_paths = []
    for file in os.listdir(folder_path):
        document_paths.append(os.path.join(folder_path, file))
    
    file_streams = [open(path, "rb") for path in document_paths]
    
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )
    
    return client, vector_store

def setup_assistant(client, vector_store):
    assistant = client.beta.assistants.create(
        instructions="You are an AI Compliance assistant tasked with helping a banker understand the complex banking guidelines. Your goal is to provide accurate and easy to understand information to the banker.",
        model="gpt-4o",  # replace with model deployment name
        tools=[{"type": "file_search"}],
        temperature=0.2,
    )
    
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    
    thread = client.beta.threads.create()
    
    return assistant, thread

def send_user_question(client, assistant, thread, question):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        count=0
        answer = ''
        number_of_messages = len(messages.data)
        print( f'Number of messages: {number_of_messages}')
        # Get the latest response only
        for message in (messages.data):
            if count!=0:
                break
            count = 1
            role = message.role  
            for content in message.content:
                if content.type == 'text':
                    response = content.text.value 
                    answer = answer + ' ' + (f'\n{role}: {response}')
        return answer
    elif run.status == 'requires_action':
        # the assistant requires calling some functions
        # and submit the tool outputs back to the run
        return "requires_action"
    else:
        return run.status


class State(rx.State):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    folder_path = os.path.join(project_root, "azure", "RBI_Guidelines_Documents")
    document_paths = []
    for file in os.listdir(folder_path):
        document_paths.append(os.path.join(folder_path, file))
    
    selected_doc: str = ""
    document_content: str = ""
    user_question: str = ""
    chat_history: list[tuple[str, str]] = []

    @rx.var
    def document_names(self) -> list[str]:
        return [os.path.basename(path) for path in self.document_paths]

    def load_document(self, doc_name: str):
        global vector_store_id
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        vector_store_id_path = os.path.join(root_path, "vector_store_id.txt")
        vector_store_id = open(vector_store_id_path, "r").read()
        self.selected_doc = doc_name
        doc_path = next((path for path in self.document_paths if os.path.basename(path) == doc_name), None)
        if doc_path and os.path.exists(doc_path):
            with open(doc_path, 'r') as file:
                self.document_content = file.read()
        else:
            self.document_content = f"Error: File not found for {doc_name}"

    def send_question(self, form_data: dict):
        global is_loading
        is_loading = True
        question = form_data.get("user_question", "")
        if question:
            self.chat_history.append(("User", question))
            print(f"Initializing vector store with {vector_store_id}...")
            client, vector_store = initialize_vector_store(vector_store_id)
            print("Setting up the assistant...")
            assistant, thread = setup_assistant(client, vector_store)
            print("Loading Answer...")
            response = send_user_question(client, assistant, thread, PROMPT+question)
            self.chat_history.append(("Chatbot", response))
            self.user_question = ""
        is_loading = False


@template(route="/chatbot", title="Compliance Chatbot")
def chatbot() -> rx.Component:
    
    return rx.center(
        rx.vstack(
            rx.heading("Compliance Chatbot", as_="h1", font_size="2em", margin_bottom="1em"),
            rx.select.root(
                rx.select.trigger(placeholder="Select a document"),
                rx.select.content(
                    rx.foreach(
                        State.document_names,
                        lambda name: rx.select.item(name, value=name)
                    )
                ),
                on_change=State.load_document,
            ),
            rx.text_area(
                value=State.document_content,
                is_read_only=True,
                height="200px",
                width="100%",
                margin_bottom="1em",
                border="1px solid #eaeaea",
                border_radius="5px",
            ),
            rx.box(
                rx.vstack(
                    rx.foreach(
                        State.chat_history,
                        lambda message: rx.vstack(
                            rx.text(f"{message[0]}:", font_weight="bold"),
                            rx.text(message[1]),
                            width="100%",
                            padding="0.5em",
                            border="1px solid #eaeaea",
                            border_radius="5px",
                            margin_bottom="0.5em",
                        )
                    ),
                    rx.cond(
                        is_loading,
                        rx.spinner(size="md"),
                    ),
                    width="100%",
                    spacing="0.5em",
                ),
                height="300px",
                overflow="auto",
                width="100%",
                border="1px solid #eaeaea",
                border_radius="5px",
                padding="1em",
                margin_bottom="1em",
            ),
            rx.form(
                rx.hstack(
                    rx.input(
                        placeholder="Ask a question...",
                        width="80%",
                        value=State.user_question,
                        on_change=State.set_user_question,
                        name="user_question",
                    ),
                    rx.button("Send", 
                              width="20%",
                                type="submit",
                                loading = is_loading,
                                ),
                    width="100%",
                ),
                on_submit=State.send_question,
            ),
            width="100%",
            max_width="800px",
            spacing="1em",
        ),
        padding="2em",
        width="100%",
        height="100vh",
    )