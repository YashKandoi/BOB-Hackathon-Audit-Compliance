import json
from ..templates import template
from .. import styles
import requests
import reflex as rx
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

counter = 1

def get_AML_guidelines():
    x = requests.get("http://127.0.0.1:8000/AML_guidelines/")
    return json.loads(x.text)['content']

class get_AML_rules(rx.State):
    text: str = ""

    def on_mount(self):
        self.text = get_AML_guidelines()


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
                rx.box(
                    rx.flex(
                        rx.heading("CHANGES", as_="h1"),
                        rx.button("Refresh", 
                                  on_click=get_AML_rules.on_mount,
                                  style=styles.overlapping_button_style,
                                ),
                        direction="row",
                        spacing="4",
                    ),
                ),
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
                rx.box(rx.markdown("Changes Summary:\n"+get_AML_rules.text),), 
                direction="column",
                spacing="4",
            ),
        )