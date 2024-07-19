import os
import time
import json
import requests
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = "95bf554acff7415f86f9563ea48537f9"

def create_client(AZURE_OPENAI_API_KEY):
    client = AzureOpenAI(
        api_key= os.getenv(AZURE_OPENAI_API_KEY),
        api_version="2024-05-01-preview",
        )
    return client

# Create assistant
def create_assistant(client):
    assistant = client.beta.assistants.create(
        instructions="You are a regulations assistant. You help a banker figure out the right compliances for whatever data they have by mapping it to rbi guidelines.",
        model="gpt-4o", # replace with model deployment name.
        tools=[{"type":"file_search"}]
        )
    return assistant

def create_vector_store(client, name):
    vector_store = client.beta.vector_stores.create(name=name)
    return vector_store

def get_vector_store(client, vector_store_id):
    vector_store = client.beta.vector_stores.retrieve(vector_store_id)
    return vector_store

# Ready the files for upload to OpenAI
def upload_files(client, vector_store, file_paths):
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )
    return file_batch

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
def add_files_to_vector_store(client, vector_store, file_batch):
    client.beta.vector_stores.file_batches.add_files(
        vector_store_id=vector_store.id, file_batch_id=file_batch.id
        )
    print(file_batch.status)
    print(file_batch.file_counts)

def use_vector_store(client, assistant, vector_store):
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
    return assistant


# Running the assistant
# Create a thread
def create_thread(client):
    thread = client.beta.threads.create()
    return thread

def use_existing_thread(client, thread_id):
    thread = client.beta.threads.retrieve(thread_id)
    return thread

# Add a user question to the thread
def add_user_question(client, thread, content):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
        )
    return message

def run_thread(client, thread, assistant):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
        )

    # Looping until the run completes or fails
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
        print(messages)
    elif run.status == 'requires_action':
    # the assistant requires calling some functions
    # and submit the tool outputs back to the run
        pass
    else:
        print(run.status)

def main():
    client = create_client(AZURE_OPENAI_API_KEY)
    assistant = create_assistant(client)
    vector_store = create_vector_store(client, "rbi-guidelines")
    file_paths = ["data/1.pdf", "data/2.pdf"]
    file_batch = upload_files(client, vector_store, file_paths)
    add_files_to_vector_store(client, vector_store, file_batch)
    assistant = use_vector_store(client, assistant, vector_store)
    thread = create_thread(client)
    add_user_question(client, thread, "What are the compliances for storing customer data?")
    run_thread(client, thread, assistant)