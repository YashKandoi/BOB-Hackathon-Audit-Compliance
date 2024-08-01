from .. import styles
from ..templates import template

import sys
import os

# Add the top-level project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from azure.userBankAccountInsightsGenerator import main as userBankAccountInsightsGenerator


import reflex as rx
import requests as rq

def get_people():
    response = rq.get("http://127.0.0.1:8000/bank_accounts/")
    data = response.json()
    return [
        [item["name"], item["age"], item["gender"], item["account_type"],item["pan_number"],item["adhaar_number"]] for item in data
    ] 

def get_user(user_id: int):
    response = rq.get("http://127.0.0.1:8000/bank_accounts/")
    data=response.json()
    for item in data:
        result=rx.cond(item["pan_number"]==user_id,item,[])
    return result

def get_account_audit_report(account_adhaar_number : str, account_type: str):
    response = rq.get("http://127.0.0.1:8000/bank_accounts/" + account_adhaar_number + "/" + account_type+"/")
    data = response.json()
    audit_report = data["insights"]
    if audit_report is None:
        response = userBankAccountInsightsGenerator(account_adhaar_number, account_type)
        return response
    return audit_report

class DownloadAuditReport(rx.State):
    is_loading: bool = False

    def download(self, name, account_adhaar_number: str, account_type: str):
        self.is_loading = True
        yield
        audit_report = get_account_audit_report(account_adhaar_number, account_type)
        self.is_loading = False
        return rx.download(
            data=audit_report,
            filename=f"{name}_{account_type}_audit_report.txt",
        )
        

class TableForEachState(rx.State):
    people: list[list] = get_people()

    def load_data(self):
        self.people = get_people()

class UserDetailState(rx.State):
    selected_person: list = []

    @staticmethod
    def fetch_person(pan_number: int):
        user_data = get_user(pan_number)
        UserDetailState.selected_person = user_data

def show_person(person: list):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(person[0]),
        rx.table.cell(person[1]),
        rx.table.cell(person[2]),
        rx.table.cell(person[3]),
        rx.table.cell(person[4]),
        rx.table.cell(person[5]),
        rx.table.cell(
            rx.button("Download", 
                      style=styles.overlapping_button_style,
                      on_click=lambda: DownloadAuditReport.download(person[0],person[5], person[3]),
                      loading=DownloadAuditReport.is_loading,
                    ), 
        ),
        align="center",
        width="100%",
    )

def view_user(user_id: int):
    UserDetailState.fetch_person(user_id)
    return rx.redirect("/user_detail", external=False)

def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )

@template(route="/users", title="Users", on_load=TableForEachState.load_data)
def users() -> rx.Component:
    return rx.flex(
        rx.box(
                rx.heading("Bank Accounts", as_="h1"),
                width="100%",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Name","user"),
                    _header_cell("Age","calendar"),
                    _header_cell("Gender","person-standing"),
                    _header_cell("Account Type","wallet-cards"),
                    _header_cell("PAN Number","credit-card"),
                    _header_cell("Adhaar Number","contact-round"),
                    _header_cell("Audit Report", "file-down"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableForEachState.people, show_person
                )
            ),
            width="100%",
            align="center",
        ),
        direction="column",
        spacing="4",
        align="center",
        width="100%",
    )
    

# @template(route="/user_detail", title="User Detail")
# def user_detail() -> rx.Component:
#     person = UserDetailState.selected_person
#     return rx.cond(person,rx.box(
#         rx.text(f"Name: {person[0]}"),
#         rx.text(f"Age: {person[1]}"),
#         rx.text(f"Gender: {person[2]}"),
#         rx.text(f"Account_type: {person[3]}"),
#         rx.text(f"PAN Number: {person[4]}"),
#         rx.text(f"Adhaar Number: {person[5]}"),
#     ),
#     rx.text("No user selected.")
#     )



