import json
from ..templates import template
from .. import styles
import requests
import reflex as rx
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

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
    


@template(route="/changes",title="Changes")
def changes()->rx.Component:
    return rx.box(
            rx.flex(
                rx.box(rx.heading("CHANGES", as_="h1"),),
                rx.box(
                    rx.upload(
                                rx.text("Upload Compliance Requirement"),
                                rx.icon(tag="upload"),
                                border="1px dotted rgb(107,99,246)",
                                padding="5em",
                                on_drop=State.handle_upload(rx.upload_files(upload_id="bank_statements")),
                                multiple=False,
                            ),
                ),
                rx.box(rx.markdown("Following are the changes:"),), 
                direction="column",
                spacing="4",
            ),
        )