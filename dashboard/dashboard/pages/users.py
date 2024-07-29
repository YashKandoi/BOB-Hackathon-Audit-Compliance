from .. import styles
from ..templates import template

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

class TableForEachState(rx.State):
    people: list[list] = get_people()

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
            rx.button("View", 
                      style=styles.overlapping_button_style), 
                    #   on_click=lambda: view_user(person[4]))  # Assuming person[3] is the user ID
        ),
    )

def view_user(user_id: int):
    UserDetailState.fetch_person(user_id)
    return rx.redirect("/user_detail", external=False)

@template(route="/users", title="Users")
def users() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Name"),
                rx.table.column_header_cell("Age"),
                rx.table.column_header_cell("Gender"),
                rx.table.column_header_cell("Account Type"),
                rx.table.column_header_cell("PAN Number"),
                rx.table.column_header_cell("Adhaar Number"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                TableForEachState.people, show_person
            )
        ),
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



