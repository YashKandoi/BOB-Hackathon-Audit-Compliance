import os
import re
import time
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = "939de1ef4c4e439dbaad834c55551410"
AZURE_OPENAI_ENDPOINT = "https://second-openai-resource.openai.azure.com/"
# VECTOR_STORE_ID = ""
# Write multiline string
PROMPT = """**Instructions:**

1. **Extract Compliance Requirements:**
    - Read the provided RBI guidelines document.
    - Identify and extract relevant compliance requirements for both KYC and AML processes.
2. **Categorize Compliance Requirements:**
    - Categorize the compliance requirements based on different user profiles :
        - Current account,
        - Savings account,
        - Salary account,
        - Fixed deposit account,
        - Recurring deposit account,
        - NRI accounts.
3. **Format the Data:**
    - Ensure the extracted compliance requirements are formatted properly.
    - Each requirement should include a brief description and any relevant details or conditions.
4. **Save the Data:**
    - Save the categorized compliance requirements in the appropriate files:
        - KYC requirements in "KYC.txt"
        - AML requirements in "AML.txt" **Output Format:**
- Each compliance requirement should be listed under the appropriate user profile category.
- Include proper citations from the RBI guidelines document for each requirement. **Example:** 
For "KYC.txt":
Individual Savings Account
Requirement: Proof of Identity 
Description: Submit a valid Aadhaar card or PAN card.
Citation: RBI Guidelines 2024, Section 2.1
Requirement: Proof of Address 
Description: Submit a recent utility bill or rent agreement.
Citation: RBI Guidelines 2024, Section 2.2
Corporate Account
Requirement: Certificate of Incorporation 
Description: Submit the certificate of incorporation for the business.
Citation: RBI Guidelines 2024, Section 3.1
Requirement: Board Resolution 
Description: Provide a board resolution authorizing the account opening.
Citation: RBI Guidelines 2024, Section 3.2
mathematica
Copy code 
For "AML.txt":
Individual Savings Account
Requirement: Transaction Monitoring 
Description: Monitor transactions exceeding INR 10 lakhs.
Citation: RBI Guidelines 2024, Section 4.1
Requirement: Suspicious Activity Reporting 
Description: Report any suspicious activities to the relevant authorities.
Citation: RBI Guidelines 2024, Section 4.2
Corporate Account
Requirement: Enhanced Due Diligence 
Description: Conduct enhanced due diligence for high-risk businesses.
Citation: RBI Guidelines 2024, Section 5.1
Requirement: Periodic Review 
Description: Perform periodic reviews of the account activities.
Citation: RBI Guidelines 2024, Section 5.2**Begin processing the RBI guidelines document and populate the AML.txt and KYC.txt files accordingly.** """

def initialize_vector_store(directory_path):
    client = AzureOpenAI(
        api_key=(AZURE_OPENAI_API_KEY),
        api_version="2024-05-01-preview",
        azure_endpoint=(AZURE_OPENAI_ENDPOINT)
    )
    
    vector_store = client.beta.vector_stores.create(name="RBI Guidelines")
    print(vector_store.id)
    
    # List all .txt files in the specified directory
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.txt')]
    
    file_streams = [open(path, "rb") for path in file_paths]
    
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    
    return client, vector_store

def setup_assistant(client, vector_store):
    assistant = client.beta.assistants.create(
        instructions="You are an AI assistant tasked with extracting and organizing compliance requirements from the latest RBI guidelines document. Your goal is to populate the AML.txt and KYC.txt files with relevant compliance requirements, categorized by different user profiles.",
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
    
def save_to_file(final_response):
    # Use regex to find the sections
    kyc_match = re.search(r'### KYC\.txt\n(.*?)### AML\.txt', final_response, re.DOTALL)
    aml_match = re.search(r'### AML\.txt\n(.*)', final_response, re.DOTALL)
    
    # Extract the KYC section
    if kyc_match:
        kyc_section = kyc_match.group(1).strip()
    else:
        kyc_section = "KYC section not found"

    # Extract the AML section
    if aml_match:
        aml_section = aml_match.group(1).strip()
    else:
        aml_section = "AML section not found"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    regulations_files_path = os.path.join(project_root,'complicanceAI', 'regulations_files')

    # Write KYC section to a file
    kyc_file_path = os.path.join(regulations_files_path, 'KYC.txt')
    with open(kyc_file_path, 'w') as kyc_file:
        kyc_file.write('KYC Rules: \n' + kyc_section)

    # Write AML section to a file
    aml_file_path = os.path.join(regulations_files_path, 'AML.txt')
    with open(aml_file_path, 'w') as aml_file:
        aml_file.write('AML Rules: \n' + aml_section)

    print("Files created successfully!")

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    regulations_files_path = os.path.join(project_root,'complicanceAI', 'regulations_files')
    for file in os.listdir(regulations_files_path):
        os.remove(os.path.join(regulations_files_path, file))
    
    directory_path = os.path.join(os.path.dirname(__file__), 'RBI_Guidelines_Documents')

    print("Initializing vector store...")
    client, vector_store = initialize_vector_store(directory_path)
    print("Setting up the assistant...")
    assistant, thread = setup_assistant(client, vector_store)
    print("Loading Answer...")
    response = send_user_question(client, assistant, thread, PROMPT)
    # remove old files
    save_to_file(response)
    print("Files created successfully!")

# if __name__ == "__main__":
#     main()