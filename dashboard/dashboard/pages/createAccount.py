
from..templates import template
from .. import styles
import json
import reflex as rx
import requests

import sys
import os

# Add the top-level project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from azure.userBankAccountInsightsGenerator import main as userBankAccountInsightsGenerator

counter = 1

class State(rx.State):
    async def handle_upload(self, files: list[rx.UploadFile]):
        upload_dir = rx.get_upload_dir() / str(counter)
        os.makedirs(upload_dir, exist_ok=True)
        for file in files:
            upload_data = await file.read()
            outfile = upload_dir / file.filename
            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
        
        return rx.window_alert(f"{files[0].filename} uploaded sucessfully!")

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict): #get input from user
        """Handle the form submit."""
        global counter
        self.form_data = form_data
        print(form_data)
        self.send_data_to_server(form_data)
        counter = counter + 1
        adhaar_number = form_data["adhaar_number"]
        account_type = form_data["account_type"]
        # self.generate_account_audit_report(adhaar_number, account_type)
        # return rx.window_alert("Account created successfully!")

    def send_data_to_server(self, form_data: dict):
        
        file_dir = rx.get_upload_dir() / str(counter)
        os.makedirs(file_dir, exist_ok=True)

        bank_statement = ""
        other_documents = ""

        for filename in os.listdir(file_dir):
            file_path = os.path.join(file_dir, filename)
            if 'bank' in filename.lower() or 'statement' in filename.lower():
                bank_statement = file_path
            else:
                other_documents = file_path

        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        super_root = os.path.dirname(project_root)
        bank_statement = os.path.join(super_root, bank_statement)
        if other_documents != "":
            other_documents = os.path.join(super_root, other_documents)
            files = {
                'bank_statement': open(bank_statement, 'rb'),
                # 'other_documents': open(other_documents, 'rb'),
            }
        else:
            files = {
                'bank_statement': open(bank_statement, 'rb'),
            }

        # Prepare the data and files to be sent
        url = 'http://127.0.0.1:8000/bank_accounts/'

        name = form_data['name']
        age = form_data['age']
        gender = form_data['gender']
        account_type = form_data['account_type']
        pan_number = form_data['pan_number']
        adhaar_number = form_data['adhaar_number']

        data = {
            'name': name,
            'age': age,
            'gender': gender,
            'account_type': account_type,
            'pan_number': pan_number,
            'adhaar_number': adhaar_number,
        }

        print(data)
        # print(files)

        response = requests.post(url, files=files, data=data)
        print(response)

        if response.status_code == 201:
            print("Data successfully sent to server.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(f"Response content: {response.content}")


    def generate_account_audit_report(self, account_adhaar_number: str, account_type: str):
        # Define the URL for the GET request
        response = requests.get("http://127.0.0.1:8000/bank_accounts/" + account_adhaar_number + "/" + account_type+"/")
        data = response.json()
        response = userBankAccountInsightsGenerator(account_adhaar_number, account_type)
        return response
        

@template(route="/createAccount", title="Create Account")
def createAccount() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.box(
                rx.heading("Create Account", as_="h1"),
                width="100%",
            ),
            rx.box(
                rx.form(
                    rx.flex(
                    rx.input(
                        placeholder="Name",
                        name="name",
                        required=True,
                    ),
                    rx.input(
                        placeholder="Age",
                        name="age",
                        required=True,
                    ),
                    rx.select(
                        ["M", "F", "O"],
                        placeholder="Select your Gender",
                        label="Gender",
                        name= "gender",
                        required=True,
                    ),
                    rx.select(
                        ["SAVINGS", "CURRENT", "SALARY", "FixedDeposit", "RecurringDeposit", "NRI"],
                        placeholder="Select Account Type",
                        label="Account Type",
                        name="account_type",
                        required=True,
                    ),
                    rx.input(
                        placeholder="Enter 10-Keyword PAN Number",
                        name="pan_number",
                        required=True,
                    ),
                    rx.input(
                        placeholder="Enter 12-digit Adhaar Number",
                        name="adhaar_number",
                        required=True,
                    ),
                    rx.flex(
                        rx.upload(
                                rx.text("Upload Bank Statement as bank_statement.pdf"),
                                rx.icon(tag="upload"),
                                border="1px dotted rgb(107,99,246)",
                                padding="5em",
                                on_drop=State.handle_upload(rx.upload_files(upload_id="bank_statements")),
                                multiple=False,
                            ),
                        rx.upload(
                                rx.text("Upload Other Documents"),
                                rx.icon(tag="upload"),
                                border="1px dotted rgb(107,99,246)",
                                padding="5em",
                                on_drop=State.handle_upload(rx.upload_files(upload_id="other_documents")),
                                 multiple=False,
                            ),
                        direction="row",
                        spacing="4",
                    ),
                    
                    rx.hstack(
                        rx.checkbox("I agree to terms and conditions", name="check"),
                    ),
                    rx.button("Submit", type="submit"),
                    direction="column",
                    spacing="4",
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
            ),
            rx.divider(),
            width="80%",
            ),
            direction="column",
            spacing="4",
            ),
            width="100%",
        ),