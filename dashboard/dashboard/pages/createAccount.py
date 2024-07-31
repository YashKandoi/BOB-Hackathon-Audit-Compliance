
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

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict): #get input from user
        """Handle the form submit."""
        self.form_data = form_data
        # self.send_data_to_server(form_data)
        # return rx.window_alert("Account created successfully!")
        # self.generate_account_audit_report(form_data["adhaar_number"], form_data["account_type"])

    def send_data_to_server(self, form_data: dict):

        json_data = json.dumps(form_data)
        print(json_data)
        url = 'http://127.0.0.1:8000/bank_accounts/'
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, data=json_data, headers=headers)
        if response.status_code == 201:
            print("Data successfully sent to server.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")

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
                        ["Male", "Female", "Other"],
                        placeholder="Select your Gender",
                        label="Gender",
                        required=True,
                    ),
                    rx.select(
                        ["Savings", "Current", "Salary", "Fixed Deposit", "Recurring Deposit", "NRI"],
                        placeholder="Select Account Type",
                        label="Account Type",
                        required=True,
                    ),
                    rx.input(
                        placeholder="PAN Number",
                        name="pan_number",
                        required=True,
                    ),
                    rx.input(
                        placeholder="Adhaar Number",
                        name="adhaar_number",
                        required=True,
                    ),
                    rx.flex(
                        rx.upload(
                            rx.text(
                                "Drag and drop Bank Statement here or click to select files"
                            ),
                            id="my_upload1",
                            border="1px dotted rgb(107,99,246)",
                            # on_click= rx.text("Upload Bank Statement"),
                        ),
                        rx.upload(
                                rx.text(
                                    "Drag and drop Other Documents here or click to select files"
                                ),
                                id="my_upload2",
                                border="1px dotted rgb(107,99,246)",
                                # on_click= rx.text("Upload Other Documents"),
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
            #rx.heading("Results"),
            #rx.text(FormState.form_data.to_string()),
            width="80%",
            ),
            direction="column",
            spacing="4",
            ),
            width="100%",
        ),