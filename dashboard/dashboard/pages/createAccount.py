
from..templates import template
from .. import styles

import reflex as rx

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict): #get input from user
        """Handle the form submit."""
        self.form_data = form_data

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
                        ),
                        rx.upload(
                                rx.text(
                                    "Drag and drop Other Documents here or click to select files"
                                ),
                                id="my_upload2",
                                border="1px dotted rgb(107,99,246)",
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