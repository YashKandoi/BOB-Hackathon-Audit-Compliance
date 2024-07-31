import os
import random
import re
import time
from openai import AzureOpenAI
import requests

AZURE_OPENAI_API_KEY = "939de1ef4c4e439dbaad834c55551410"
AZURE_OPENAI_ENDPOINT = "https://second-openai-resource.openai.azure.com/"
# VECTOR_STORE_ID = ""

# create a function to output a random number between 1 and 100
def random_number():
    # return name from Account Details when it is integrated in JSON format
    return random.randint(1, 100)

def initialize_vector_store(file_paths):
    client = AzureOpenAI(
        api_key=(AZURE_OPENAI_API_KEY),
        api_version="2024-05-01-preview",
        azure_endpoint=(AZURE_OPENAI_ENDPOINT)
    )
    
    vector_store = client.beta.vector_stores.create(name=f"User Bank Account Insights-{random_number()}")
    print(vector_store.id)
    
    file_streams = [open(path, "rb") for path in file_paths]
    
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    
    return client, vector_store

def setup_assistant(client, vector_store):
    assistant = client.beta.assistants.create(
        instructions="You are a compliance agent responsible for mapping user's bank account details with the compliances and reporting potential compliance issues and giving general insights",
        model="gpt-4o",  # replace with model deployment name
        tools=[{"type": "file_search"}],
        temperature=0.1,
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
        content=question,
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
    
def save_to_file(final_response,account_holder_name,account_type):
    # Write response to a file
    with open(f'azure/AuditReports/AuditReport-{account_holder_name}-{account_type}.txt', 'w') as file:
        file.write(final_response)

def main(account_holder_adhaar_number, account_type):

    # Getting User Account Details and their documents
    print("Fetching account details...")
    account = requests.get("http://127.0.0.1:8000/bank_accounts/"+account_holder_adhaar_number+"/"+account_type+"/")
    ACCOUNT_DETAILS = account.json()
    print(ACCOUNT_DETAILS)
    media_base_path = "complicanceAI/complicanceAI"
    bank_statement = media_base_path + ACCOUNT_DETAILS.get("bank_statement")
    if(ACCOUNT_DETAILS.get("other_documents") == None):
        list_of_file_paths = [bank_statement, "complicanceAI/regulations_files/KYC.txt", "complicanceAI/regulations_files/AML.txt"]
    else:
        other_documents = media_base_path + ACCOUNT_DETAILS.get("other_documents")
        list_of_file_paths = [bank_statement, other_documents, "complicanceAI/regulations_files/KYC.txt", "complicanceAI/regulations_files/AML.txt"]
    
    PROMPT = f"""You are tasked with generating compliance insights for a bank account based on account details, KYC guidelines, AML guidelines, and the bank statement.   
    The account details are: - {ACCOUNT_DETAILS}.  
    The bank statement has been uploaded.  
    The KYC guidelines are also uploaded.  
    The AML guidelines are also uploaded.  
    Provide a comprehensive compliance insight report that includes:   
    1. KYC compliance status and any missing documents.   
    2. AML compliance status and any suspicious transactions.  
    3. Recommendations for maintaining compliance.
    """

    print("Initializing vector store...")
    client, vector_store = initialize_vector_store(list_of_file_paths)
    print("Setting up the assistant...")
    assistant, thread = setup_assistant(client, vector_store)
    print("Loading Answer...")
    response = send_user_question(client, assistant, thread, PROMPT)
    requests.put(
        "http://127.0.0.1:8000/bank_accounts/"+account_holder_adhaar_number+"/"+account_type+"/",
        data={
        "name": ACCOUNT_DETAILS.get("name"),
        "age": ACCOUNT_DETAILS.get("age"),
        "gender": ACCOUNT_DETAILS.get("gender"),
        "account_type": ACCOUNT_DETAILS.get("account_type"),
        "pan_number": ACCOUNT_DETAILS.get("pan_number"),
        "adhaar_number": ACCOUNT_DETAILS.get("adhaar_number"),
        "insights":response
    })
    account_holder_name = ACCOUNT_DETAILS.get("name")
    save_to_file(response,account_holder_name,account_type)
    print("Audit Report Insights added successfully!")
    return response

# if __name__ == '__main__':
#     main("123412341234", "SAVINGS")